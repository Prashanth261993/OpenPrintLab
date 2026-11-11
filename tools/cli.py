"""Command-line entry point. Run from the repository root."""

import argparse
import json
from pathlib import Path
import sys

from tools.catalog import build_model, load_catalog, parameter_schema, write_build


def main():
    parser = argparse.ArgumentParser(description="OpenPrintLab local model tools; no printer control")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List original models")
    commands.add_parser("templates", help="List original models and optional CAD generators")
    commands.add_parser("patterns", help="Read curated review patterns and source-specific evidence")
    pattern = commands.add_parser("pattern", help="Read one pattern; not a validated design or rating")
    pattern.add_argument("identifier")
    for name in ("inspect-stl", "inspect-variant"):
        inspection = commands.add_parser(name, help="Read-only geometry diagnostics; not slicing or safety evidence")
        inspection.add_argument("target")
        inspection.add_argument("--mode", choices=["part", "plate", "assembly"], default="part")
        inspection.add_argument("--margin", type=float, default=0, help="Reserved XY edge margin in mm")
        inspection.add_argument("--overhang", type=float, default=45, help="Warning angle from vertical in degrees")
        inspection.add_argument("--clearance", type=float, default=0, help="Conservative component-pair clearance threshold in mm")
    template = commands.add_parser("template", help="Describe a template and its supported parameters")
    template.add_argument("model")
    customize = commands.add_parser("customize", help="Create a new named variant with a real preview; never overwrite")
    customize.add_argument("model")
    customize.add_argument("--variant", required=True)
    customize.add_argument("--set", action="append", default=[], metavar="NAME=NUMBER")
    customize.add_argument("--params", type=Path, help="Effective parameter JSON object from a prior variant")
    customize.add_argument("--output", type=Path, help="Variant root; defaults to this clone's build/variants")
    advice = commands.add_parser("guidance", help="Ask for actual setup before model-aware starting suggestions")
    advice.add_argument("variant")
    advice.add_argument("--output", type=Path)
    advice.add_argument("--printer")
    advice.add_argument("--nozzle", type=float)
    advice.add_argument("--plate")
    advice.add_argument("--material")
    advice.add_argument("--use", choices=["desk-organization", "hobby-sorting", "learning", "paper-display"])
    for command in ("build", "check", "parameters"):
        sub = commands.add_parser(command)
        sub.add_argument("model")
        if command != "parameters":
            sub.add_argument("--set", action="append", default=[], metavar="NAME=NUMBER")
        if command == "build":
            sub.add_argument("--output", default="build", help="Output directory (default: build)")
    args = parser.parse_args()
    try:
        if args.command == "list":
            result = load_catalog()
        elif args.command in ("patterns", "pattern"):
            from tools.patterns import describe_pattern, list_patterns
            result = list_patterns() if args.command == "patterns" else describe_pattern(args.identifier)
        elif args.command in ("inspect-stl", "inspect-variant"):
            from tools.diagnostics import inspect_file, inspect_variant
            inspect = inspect_file if args.command == "inspect-stl" else inspect_variant
            result = inspect(args.target, mode=args.mode, margin_mm=args.margin,
                             overhang_degrees=args.overhang, clearance_mm=args.clearance)
        elif args.command in ("templates", "template", "guidance"):
            from tools.variants import describe_template, guidance, list_templates
            if args.command == "templates":
                result = list_templates()
            elif args.command == "template":
                result = describe_template(args.model)
            else:
                setup = {"printer": args.printer, "nozzle_mm": args.nozzle, "plate": args.plate,
                         "material": args.material, "use": args.use}
                result = guidance(args.variant, setup, args.output)
        elif args.command == "parameters":
            result = parameter_schema(args.model)
        else:
            overrides = {}
            if args.command == "customize" and args.params:
                overrides = json.loads(args.params.read_text(encoding="utf-8"))
                if not isinstance(overrides, dict):
                    raise ValueError("Parameter file must contain a JSON object")
            specified = set()
            for pair in args.set:
                key, value = pair.split("=", 1)
                if key in specified:
                    raise ValueError(f"Duplicate parameter: {key}")
                specified.add(key)
                overrides[key] = float(value)
            if args.command == "customize":
                from tools.variants import create_variant
                result = create_variant(args.model, args.variant, overrides, args.output)
            elif args.command == "build":
                result = write_build(args.model, args.output, overrides)
            else:
                _, result = build_model(args.model, overrides)
        print(json.dumps(result, indent=2))
        if args.command in ("inspect-stl", "inspect-variant") and result["has_errors"]:
            return 1
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"OpenPrintLab: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
