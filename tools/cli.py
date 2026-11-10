"""Command-line entry point. Run from the repository root."""

import argparse
import json
import sys

from tools.catalog import build_model, load_catalog, parameter_schema, write_build


def main():
    parser = argparse.ArgumentParser(description="OpenPrintLab local model tools; no printer control")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List original models")
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
        elif args.command == "parameters":
            result = parameter_schema(args.model)
        else:
            overrides = {}
            for pair in args.set:
                key, value = pair.split("=", 1)
                if key in overrides:
                    raise ValueError(f"Duplicate parameter: {key}")
                overrides[key] = float(value)
            if args.command == "build":
                result = write_build(args.model, args.output, overrides)
            else:
                _, result = build_model(args.model, overrides)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError) as exc:
        print(f"OpenPrintLab: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
