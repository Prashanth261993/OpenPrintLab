"""Optional local stdio MCP. Uses the same catalog and build checks as the CLI."""

from mcp.server.fastmcp import FastMCP
from pydantic import StrictFloat, StrictInt

from tools.catalog import ROOT, build_model, get_model, load_catalog, parameter_schema, write_build
from tools import variants

mcp = FastMCP("OpenPrintLab")
_CAD_ENABLED = False


@mcp.tool()
def design_patterns(pattern_id: str | None = None) -> dict:
    """Read curated patterns with pinned source observations, not safety ratings.

    None lists all patterns. Unknown identifiers fail rather than substituting advice.
    Local physical/slicer evidence is not promoted from upstream reports.
    """
    from tools.patterns import describe_pattern, list_patterns
    return list_patterns() if pattern_id is None else describe_pattern(pattern_id)


@mcp.tool()
def list_models() -> dict:
    """List original designs; none are physically print-tested."""
    return load_catalog()


@mcp.tool()
def describe_model(model_id: str) -> dict:
    """Read print notes and allowed dimensions before proposing changes."""
    return {"model": get_model(model_id), "parameters": parameter_schema(model_id)}


@mcp.tool()
def check_model(model_id: str, parameters: dict[str, float] | None = None) -> dict:
    """Generate in memory and check geometry; no files or printer operations."""
    return build_model(model_id, parameters)[1]


@mcp.tool()
def export_model(model_id: str, parameters: dict[str, float] | None = None) -> dict:
    """Write STL and report only inside this clone's build/mcp directory.

    Repeated exports of the same model replace its previous export.
    No arbitrary paths, shell commands, network calls or printer control.
    """
    get_model(model_id)
    output = ROOT / "build" / "mcp"
    if output.resolve() != ROOT.resolve() / "build" / "mcp":
        raise ValueError("MCP output path must not use symlinks")
    for suffix in (".stl", ".report.json"):
        if (output / f"{model_id}{suffix}").is_symlink():
            raise ValueError("MCP output files must not be symlinks")
    report = write_build(model_id, output, parameters)
    return {"stl": str(output / f"{model_id}.stl"), "report": report}


def _variant_output():
    output = variants.DEFAULT_OUTPUT
    if output.resolve() != ROOT.resolve() / "build" / "variants":
        raise ValueError("Variant output root must not use symlinks")
    return output


@mcp.tool()
def inspect_variant(variant_name: str, mode: str = "part",
                    margin_mm: StrictFloat | StrictInt = 0,
                    overhang_degrees: StrictFloat | StrictInt = 45,
                    clearance_mm: StrictFloat | StrictInt = 0) -> dict:
    """Read-only screening of an existing variant's exact STL inside build/variants.

    No arbitrary paths or repair. Inspect findings/has_errors; warnings are not
    slicer or mechanical evidence, and overlapping bounds need an exact check.
    """
    from tools.diagnostics import inspect_variant as inspect
    return inspect(variant_name, root=_variant_output(), mode=mode, margin_mm=margin_mm,
                   overhang_degrees=overhang_degrees, clearance_mm=clearance_mm)


@mcp.tool()
def list_templates() -> dict:
    """Discover builtin and optional CAD generators without importing CadQuery."""
    return {"templates": variants.list_templates(), "available_backends": ["builtin", "cadquery"] if _CAD_ENABLED else ["builtin"]}


@mcp.tool()
def describe_template(template_id: str) -> dict:
    """Get bounds, default dimensions, supported styles and intended-use limits."""
    return variants.describe_template(template_id)


@mcp.tool()
def create_variant(template_id: str, variant_name: str, parameters: dict[str, StrictFloat | StrictInt] | None = None) -> dict:
    """Create checked STL, optional STEP, real SVG/HTML preview and passport.

    Requires approval to write local files. Uses build/variants only. Existing
    names are refused, not overwritten. CAD templates need the optional backend.
    No natural-language parser, paid API, arbitrary code execution or printer control.
    """
    if variants.describe_template(template_id)["backend"] == "cadquery" and not _CAD_ENABLED:
        raise ValueError("CAD tools require starting this server with --cadquery using the optional CAD environment. Builtin tools remain available.")
    return variants.create_variant(template_id, variant_name, parameters, _variant_output())


@mcp.tool()
def variant_guidance(variant_name: str, printer: str | None = None, nozzle_mm: float | None = None,
                     plate: str | None = None, material: str | None = None, intended_use: str | None = None) -> dict:
    """Ask for missing actual setup, or return bounded cited starting suggestions.

    Intended use is desk-organization, hobby-sorting, learning or paper-display,
    subject to the model's limits. Suggestions never promote evidence status.
    """
    setup = {"printer": printer, "nozzle_mm": nozzle_mm, "plate": plate, "material": material, "use": intended_use}
    return variants.guidance(variant_name, setup, _variant_output())


def main():
    import argparse
    global _CAD_ENABLED
    parser = argparse.ArgumentParser(description="Local OpenPrintLab stdio MCP; optional CAD is explicit.")
    parser.add_argument("--cadquery", action="store_true", help="Initialize the optional native CAD stack before starting the async server")
    args = parser.parse_args()
    if args.cadquery:
        try:
            variants._cadquery()
        except ValueError as exc:
            parser.error(str(exc))
        _CAD_ENABLED = True
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
