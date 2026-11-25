import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

from tools import bambu_project as bp
from tools.catalog import build_model
from tools.geometry import decode_stl


class BambuProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profiles = self.root / "BBL"
        self.documents = {
            "machine": {
                "base": {
                    "printable_area": ["0x0", "256x0", "256x256", "0x256"],
                    "printable_height": "256", "bed_exclude_area": [],
                    "extruder_type": ["Direct Drive"], "default_nozzle_volume_type": ["Standard"],
                },
                bp.PRINTER: {
                    "inherits": "base", "printer_model": "Bambu Lab P2S",
                    "printer_variant": "0.4", "nozzle_diameter": ["0.4"],
                },
            },
            "process": {
                "base": {
                    "layer_height": "0.2", "wall_loops": "2", "sparse_infill_density": "15%",
                    "top_shell_layers": "4", "bottom_shell_layers": "3",
                    "sparse_infill_pattern": "grid", "enable_support": "0", "brim_type": "no_brim",
                },
                bp.PROCESS: {
                    "inherits": "base", "compatible_printers": [bp.PRINTER],
                    "print_extruder_variant": [bp.EXTRUDER],
                },
            },
            "filament": {
                "base": {
                    "filament_type": ["PLA"], "filament_id": "synthetic-not-for-slicing",
                    "textured_plate_temp": ["55"], "textured_plate_temp_initial_layer": ["55"],
                },
                "variant": {"filament_extruder_variant": [bp.EXTRUDER]},
                bp.FILAMENT: {
                    "inherits": "base", "include": ["variant"], "compatible_printers": [bp.PRINTER],
                },
            },
        }
        for kind, documents in self.documents.items():
            for name, data in documents.items():
                self.write_profile(kind, name, data)
        stl, report = build_model("step-study")
        self.stl, self.report = self.root / "source.stl", self.root / "report.json"
        self.stl.write_bytes(stl)
        self.report.write_text(json.dumps(report))
        self.output = self.root / "project.3mf"
        self.kwargs = {
            "profiles_dir": self.profiles, "studio_version": bp.STUDIO_VERSION,
            "printer": bp.PRINTER, "process": bp.PROCESS, "filament": bp.FILAMENT,
            "plate": bp.PLATE, "nozzle_mm": 0.4, "extruder_variant": bp.EXTRUDER,
            "translation_xy": [104, 116],
        }

    def write_profile(self, kind, name, data):
        path = self.profiles / kind / (name + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({
            "type": kind, "name": name, "from": "system",
            "instantiation": "true" if name in (bp.PRINTER, bp.PROCESS, bp.FILAMENT) else "false", **data,
        }))
        return path

    def export(self, **changes):
        return bp.export_project(self.stl, self.report, self.output, **(self.kwargs | changes))

    def rewrite(self, parts, name="changed.3mf"):
        path = self.root / name
        with zipfile.ZipFile(path, "w") as archive:
            for key, value in parts.items():
                archive.writestr(key, value)
        return path

    def test_exact_mesh_settings_passport_and_deterministic_non_overwrite(self):
        before = self.stl.read_bytes(), self.report.read_bytes()
        receipt = self.export(overrides={"wall_loops": 3, "layer_height": 0.2, "sparse_infill_density": "20%"})
        manifest = bp.inspect_project(self.output)
        self.assertEqual(manifest["checks"]["dimensions_mm"], [48.0, 24.0, 16.0])
        self.assertEqual(manifest["profiles"]["overrides"]["wall_loops"], "3")
        self.assertEqual(manifest["settings"]["different_settings_to_system"],
                         ["sparse_infill_density;wall_loops", "", ""])
        self.assertEqual(manifest["settings"]["layer_height"], "0.2")
        self.assertEqual(manifest["settings"]["nozzle_volume_type"], ["Standard"])
        self.assertFalse(manifest["validation"]["app_open_verified"])
        self.assertFalse(manifest["validation"]["slicer_checked"])
        parts = bp._archive(self.output)
        self.assertEqual(parts["Metadata/openprintlab/source.stl"], before[0])
        self.assertEqual(parts["Metadata/openprintlab/source.report.json"], before[1])
        triangles, transforms = bp._mesh_and_transform(parts)
        self.assertEqual(triangles, decode_stl(before[0]))
        self.assertEqual(transforms[1][-3:], [104, 116, 0])
        self.assertEqual((self.stl.read_bytes(), self.report.read_bytes()), before)
        payload = self.output.read_bytes()
        with self.assertRaises(FileExistsError):
            self.export()
        self.assertEqual(payload, self.output.read_bytes())
        self.output = self.root / "second.3mf"
        other = self.export(overrides={"wall_loops": 3, "layer_height": 0.2, "sparse_infill_density": "20%"})
        self.assertEqual(receipt["sha256"], other["sha256"])
        uuids = []
        for name, data in parts.items():
            if name.endswith(".model"):
                uuids.extend(n.get(f"{{{bp.PRODUCTION}}}UUID") for n in ET.fromstring(data).iter()
                             if n.get(f"{{{bp.PRODUCTION}}}UUID"))
        self.assertEqual(len(uuids), 5)
        self.assertEqual(len(uuids), len(set(uuids)))

    def test_roundtrip_retains_full_float32_coordinates_without_rounding(self):
        stl, report = build_model("pocket-tray", {"wall": 2.1234567})
        self.stl.write_bytes(stl)
        self.report.write_text(json.dumps(report))
        self.export(translation_xy=[80, 80])
        self.assertEqual(bp._mesh_and_transform(bp._archive(self.output))[0], decode_stl(stl))

    def test_profile_dependencies_and_hashes_include_parents_and_includes(self):
        manifest = self.export()["manifest"]
        self.assertEqual(bp.verify_profile_sources(self.output, self.profiles),
                         {"profile_source_hashes_match": True, "active_studio_presets_verified": False})
        records = manifest["profiles"]["files"]["filament"]
        self.assertEqual(len(records), 3)
        effective, _ = bp.resolve_profile(self.profiles, "filament", bp.FILAMENT)
        self.assertEqual(effective["filament_extruder_variant"], [bp.EXTRUDER])
        before = manifest["profiles"]["resolved_sha256"]["filament"]
        self.write_profile("filament", "base", self.documents["filament"]["base"] | {"textured_plate_temp": ["60"]})
        with self.assertRaisesRegex(ValueError, "sources changed"):
            bp.verify_profile_sources(self.output, self.profiles)
        self.output = self.root / "new-profiles.3mf"
        self.assertNotEqual(before, self.export()["manifest"]["profiles"]["resolved_sha256"]["filament"])

    def test_implicit_app_default_requires_explicit_override(self):
        baseline = dict(self.documents["process"]["base"])
        del baseline["brim_type"]
        self.write_profile("process", "base", baseline)
        with self.assertRaisesRegex(ValueError, "Missing supported process setting: brim_type"):
            self.export()
        manifest = self.export(overrides={"brim_type": "no_brim"})["manifest"]
        self.assertEqual(manifest["settings"]["different_settings_to_system"], ["brim_type", "", ""])

    def test_invalid_or_ambiguous_profiles_do_not_fallback(self):
        for kind, name, change in (
            ("machine", bp.PRINTER, {"inherits": "absent"}),
            ("machine", bp.PRINTER, {"inherits": bp.PRINTER}),
            ("machine", bp.PRINTER, {"inherits": "../escape"}),
            ("machine", bp.PRINTER, {"printer_model": "Bambu Lab P1S"}),
            ("machine", bp.PRINTER, {"bed_exclude_area": ["0x0", "20x20"]}),
            ("process", bp.PROCESS, {"compatible_printers": []}),
            ("process", bp.PROCESS, {"compatible_printers_condition": "true"}),
            ("filament", bp.FILAMENT, {"filament_type": ["PETG"]}),
            ("filament", bp.FILAMENT, {"include": ["absent"]}),
            ("filament", bp.FILAMENT, {"from": "user"}),
            ("filament", bp.FILAMENT, {"instantiation": "false"}),
        ):
            with self.subTest(change=change):
                original = self.documents[kind][name]
                self.write_profile(kind, name, original | change)
                with self.assertRaises(ValueError):
                    self.export()
                self.assertFalse(self.output.exists())
                self.write_profile(kind, name, original)
        duplicate = self.profiles / "filament" / "duplicate"
        duplicate.mkdir()
        source = self.profiles / "filament" / (bp.FILAMENT + ".json")
        (duplicate / source.name).write_bytes(source.read_bytes())
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.export()

    def test_invalid_choices_and_overrides_fail_without_output(self):
        for changes in (
            {"printer": "P2S"}, {"printer": "Bambu Lab P1S 0.4 nozzle"},
            {"nozzle_mm": True}, {"nozzle_mm": 0.6}, {"plate": "guess"},
            {"studio_version": "02.09.01.70"}, {"filament": "Generic PLA"},
            {"extruder_variant": "Direct Drive High Flow"},
            {"translation_xy": [float("nan"), 0]}, {"translation_xy": [0, 0]},
            {"translation_xy": [230, 230]}, {"translation_xy": [1, 2, 3]},
            {"overrides": {"wall_loops": 2.5}}, {"overrides": {"layer_height": float("inf")}},
            {"overrides": {"wall_loops": True}}, {"overrides": {"sparse_infill_density": "90%"}},
            {"overrides": {"enable_support": "1"}}, {"overrides": {"brim_type": "auto_brim"}},
            {"overrides": {"machine_start_gcode": "forbidden"}},
            {"overrides": {"nozzle_temperature": "220"}},
            {"overrides": {"unknown": "anything"}},
            {"overrides": []},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.export(**changes)
            self.assertFalse(self.output.exists())

    def test_bad_mesh_and_passport_are_rejected_without_repair(self):
        original = self.stl.read_bytes()
        for data in (b"", original[:-1], original + b"x"):
            self.stl.write_bytes(data)
            with self.assertRaises(ValueError):
                self.export()
        self.stl.write_bytes(original)
        passport = json.loads(self.report.read_text())
        for change in ({"units": "inch"}, {"sha256": "0" * 64}, {"passport": {}},
                       {"checks": {"dimensions_mm": [1, 1, 1]}}, {"validation": {"software_checked": False}}):
            self.report.write_text(json.dumps(passport | change))
            with self.assertRaises(ValueError):
                self.export()
            self.assertFalse(self.output.exists())
        self.report.write_text('{"units":"mm","units":"inch"}')
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.export()

    def test_member_hashes_relationships_and_settings_are_checked(self):
        self.export()
        parts = bp._archive(self.output)
        changed = parts | {"Metadata/project_settings.config": b"{}"}
        with self.assertRaisesRegex(ValueError, "hash"):
            bp.inspect_project(self.rewrite(changed))
        # Even a matching changed-member hash cannot mask a broken relationship.
        changed = copy.deepcopy(parts)
        changed["_rels/.rels"] = bp._relationships("/missing.model")
        manifest = json.loads(changed["Metadata/openprintlab/manifest.json"])
        manifest["members_sha256"]["_rels/.rels"] = bp._hash(changed["_rels/.rels"])
        changed["Metadata/openprintlab/manifest.json"] = json.dumps(manifest).encode()
        with self.assertRaisesRegex(ValueError, "relationship"):
            bp.inspect_project(self.rewrite(changed))
        with self.assertRaisesRegex(ValueError, "G-code"):
            bp.inspect_project(self.rewrite(parts | {"Metadata/plate_1.gcode": b"not shipped"}))
        changed = copy.deepcopy(parts)
        changed["Metadata/model_settings.config"] = changed["Metadata/model_settings.config"].replace(
            b'key="extruder" value="1"', b'key="extruder" value="2"')
        manifest = json.loads(changed["Metadata/openprintlab/manifest.json"])
        manifest["members_sha256"]["Metadata/model_settings.config"] = bp._hash(changed["Metadata/model_settings.config"])
        changed["Metadata/openprintlab/manifest.json"] = json.dumps(manifest).encode()
        with self.assertRaisesRegex(ValueError, "extruder differs"):
            bp.inspect_project(self.rewrite(changed))
        changed = copy.deepcopy(parts)
        config = json.loads(changed["Metadata/project_settings.config"])
        config["machine_start_gcode"] = "unexpected"
        changed["Metadata/project_settings.config"] = json.dumps(config).encode()
        manifest = json.loads(changed["Metadata/openprintlab/manifest.json"])
        manifest["settings"] = config
        manifest["members_sha256"]["Metadata/project_settings.config"] = bp._hash(changed["Metadata/project_settings.config"])
        changed["Metadata/openprintlab/manifest.json"] = json.dumps(manifest).encode()
        with self.assertRaisesRegex(ValueError, "arbitrary config"):
            bp.inspect_project(self.rewrite(changed))

    def test_saved_copy_comparison_detects_geometry_and_setting_changes(self):
        self.export()
        parts = bp._archive(self.output)
        saved = self.rewrite(parts, "saved.3mf")
        result = bp.compare_saved_project(self.output, saved)
        self.assertTrue(result["geometry_and_placement_retained"])
        self.assertFalse(result["slicer_checked"])
        cfg = json.loads(parts["Metadata/project_settings.config"])
        cfg["printer_settings_id"] = "Bambu Lab P1S 0.4 nozzle"
        changed = parts | {"Metadata/project_settings.config": json.dumps(cfg).encode()}
        with self.assertRaisesRegex(ValueError, "settings differ"):
            bp.compare_saved_project(self.output, self.rewrite(changed))
        changed = parts | {"3D/3dmodel.model": parts["3D/3dmodel.model"].replace(b"104.0 116.0", b"105.0 116.0")}
        with self.assertRaisesRegex(ValueError, "geometry/placement"):
            bp.compare_saved_project(self.output, self.rewrite(changed))

    def test_saved_copy_reordered_mesh_with_recentered_coordinates(self):
        self.export()
        parts = bp._archive(self.output)
        root = ET.fromstring(parts["3D/Objects/object_1.model"])
        vertices = root.find(f".//{{{bp.CORE}}}vertices")
        for point in vertices:
            point.set("x", repr(float(point.get("x")) - 24))
            point.set("y", repr(float(point.get("y")) - 12))
        faces = root.find(f".//{{{bp.CORE}}}triangles")
        faces[:] = list(reversed(faces))
        parts["3D/Objects/object_1.model"] = ET.tostring(root)
        root = ET.fromstring(parts["3D/3dmodel.model"])
        component = root.find(f".//{{{bp.CORE}}}component")
        component.set("transform", "1 0 0 0 1 0 0 0 1 24 12 0")
        parts["3D/3dmodel.model"] = ET.tostring(root)
        del parts["Metadata/openprintlab/source.report.json"]
        result = bp.compare_saved_project(self.output, self.rewrite(parts))
        self.assertTrue(result["geometry_and_placement_retained"])
        self.assertFalse(result["source_passport_retained_by_studio"])

    def test_actual_studio_saved_fragments_retain_geometry_and_explicit_settings(self):
        fixture = json.loads((Path(__file__).parent / "fixtures" / "bambu_project"
                              / "studio-02.09.02.62-save.json").read_text())
        self.write_profile("filament", "base", self.documents["filament"]["base"] | {"filament_id": "GFA00"})
        self.export(overrides={"wall_loops": 3, "sparse_infill_density": "20%",
                               "brim_type": "no_brim", "top_shell_layers": 5})
        saved = self.rewrite({
            "3D/3dmodel.model": fixture["root_model_xml"].encode(),
            "3D/Objects/object_1.model": fixture["object_model_xml"].encode(),
            "Metadata/project_settings.config": json.dumps(fixture["explicit_settings"]).encode(),
        })
        result = bp.compare_saved_project(self.output, saved)
        self.assertTrue(result["geometry_and_placement_retained"])
        self.assertTrue(result["explicit_settings_retained"])
        self.assertEqual(result["triangles"], 72)
        self.assertFalse(result["source_passport_retained_by_studio"])

    def test_defective_mesh_with_matching_hash_is_not_silently_repaired(self):
        from tools.geometry import encode_stl
        stl = encode_stl(decode_stl(self.stl.read_bytes())[:-1])
        report = json.loads(self.report.read_text())
        report["sha256"] = bp._hash(stl)
        report["evidence"]["scope"]["stl_sha256"] = bp._hash(stl)
        self.stl.write_bytes(stl)
        self.report.write_text(json.dumps(report))
        with self.assertRaisesRegex(ValueError, "open, non-manifold"):
            self.export()
        self.assertFalse(self.output.exists())

    def test_cli_requires_explicit_inputs_and_reports_errors(self):
        result = subprocess.run([sys.executable, "-m", "tools.bambu_project", "supported"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["printer"], bp.PRINTER)
        result = subprocess.run([sys.executable, "-m", "tools.bambu_project", "export"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--filament", result.stderr)
        args = [sys.executable, "-m", "tools.bambu_project", "export",
                "--stl", str(self.stl), "--report", str(self.report), "--output", str(self.output),
                "--translate", "104", "116", "--set", "wall_loops=3"]
        for key, value in self.kwargs.items():
            if key != "translation_xy":
                args.extend(["--" + key.replace("_", "-"), str(value)])
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["manifest"]["settings"]["wall_loops"], "3")
        result = subprocess.run(args, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("already exists", result.stderr)


if __name__ == "__main__":
    unittest.main()
