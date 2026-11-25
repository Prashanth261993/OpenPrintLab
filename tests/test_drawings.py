import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from tools.drawings import draw_stl
from tools.geometry import mesh_union, encode_stl


class DrawingTests(unittest.TestCase):
    def test_orthographic_dimensions_come_from_exported_mesh(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "part.stl"
            data = encode_stl(mesh_union([(5, 7, 0, 25, 37, 8)]))
            source.write_bytes(data)
            result = draw_stl(source, root / "drawings")
            self.assertEqual(result["views"]["top"]["dimensions_mm"], [20, 30])
            self.assertEqual(result["views"]["front"]["dimensions_mm"], [20, 8])
            self.assertEqual(result["views"]["right"]["dimensions_mm"], [30, 8])
            for view, record in result["views"].items():
                svg = ET.parse(root / "drawings" / f"{view}.svg")
                numbers = [float(e.attrib["data-dimension-mm"]) for e in svg.iter()
                           if "data-dimension-mm" in e.attrib]
                self.assertEqual(numbers, record["dimensions_mm"])
            self.assertEqual(source.read_bytes(), data)
            with self.assertRaises(FileExistsError):
                draw_stl(source, root / "drawings")

    def test_bad_mesh_creates_no_drawing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "bad.stl"
            source.write_bytes(encode_stl(mesh_union([(0, 0, 0, 2, 2, 2)])[:-1]))
            with self.assertRaisesRegex(ValueError, "errors"):
                draw_stl(source, root / "out")
            self.assertFalse((root / "out").exists())
