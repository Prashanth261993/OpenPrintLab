"""Optional local stdio MCP. Uses the same catalog and build checks as the CLI."""

from mcp.server.fastmcp import FastMCP

from tools.catalog import ROOT, build_model, get_model, load_catalog, parameter_schema, write_build

mcp = FastMCP("OpenPrintLab")


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


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
