"""Exercise the real optional SDK over stdio, including export and rejection."""

import asyncio
import json
import importlib.util
from pathlib import Path
import sys
import shutil
import uuid

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tools.catalog import ROOT, build_model
from tools.variants import render_index


async def check():
    arguments = ["-m", "tools.mcp_server"]
    if importlib.util.find_spec("cadquery"):
        arguments.append("--cadquery")
    server = StdioServerParameters(command=sys.executable, args=arguments, cwd=str(ROOT))
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await asyncio.wait_for(session.initialize(), timeout=60)
            tools = await session.list_tools()
            assert {tool.name for tool in tools.tools} == {
                "list_models", "describe_model", "check_model", "export_model",
                "list_templates", "describe_template", "create_variant", "variant_guidance",
            }
            result = await session.call_tool("describe_model", {"model_id": "pocket-tray"})
            assert not result.isError
            described = json.loads(result.content[0].text)
            assert described["parameters"]["length"]["default"] == 96
            result = await session.call_tool("check_model", {"model_id": "pocket-tray", "parameters": {"length": 120}})
            assert not result.isError
            checked = json.loads(result.content[0].text)
            assert checked["checks"]["dimensions_mm"] == [120, 64, 16]
            assert checked["validation"]["physical_print_tested"] is False
            result = await session.call_tool("export_model", {"model_id": "step-study"})
            assert not result.isError
            exported = json.loads(result.content[0].text)
            path = Path(exported["stl"])
            assert path == ROOT / "build" / "mcp" / "step-study.stl"
            assert path.read_bytes() == build_model("step-study")[0]
            for name, arguments in (
                ("check_model", {"model_id": "pocket-tray", "parameters": {"length": 999}}),
                ("check_model", {"model_id": "pocket-tray", "parameters": {"unknown": 1}}),
                ("export_model", {"model_id": "../outside"}),
            ):
                result = await session.call_tool(name, arguments)
                assert result.isError, (name, arguments)
            result = await session.call_tool("list_templates")
            assert not result.isError
            assert len(json.loads(result.content[0].text)["templates"]) == 7
            name = "mcp-trial-" + uuid.uuid4().hex[:8]
            output = ROOT / "build" / "variants" / name
            try:
                result = await session.call_tool("create_variant", {"template_id": "pocket-tray", "variant_name": name})
                assert not result.isError
                created = json.loads(result.content[0].text)
                assert Path(created["stl"]).is_file()
                assert (output / "index.html").is_file()
                result = await session.call_tool("create_variant", {"template_id": "pocket-tray", "variant_name": name})
                assert result.isError
                result = await session.call_tool("variant_guidance", {"variant_name": name})
                assert json.loads(result.content[0].text)["status"] == "needs_input"
            finally:
                if output.is_dir():
                    shutil.rmtree(output)
                    render_index(output.parent)
            if importlib.util.find_spec("cadquery"):
                name = "mcp-cad-" + uuid.uuid4().hex[:8]
                output = ROOT / "build" / "variants" / name
                try:
                    result = await asyncio.wait_for(session.call_tool("create_variant", {
                        "template_id": "rounded-organizer", "variant_name": name,
                        "parameters": {"length": 140, "radius": 8, "compartments": 3},
                    }), timeout=60)
                    assert not result.isError
                    created = json.loads(result.content[0].text)
                    assert created["report"]["backend"]["name"] == "cadquery"
                    assert Path(created["step"]).is_file()
                    result = await session.call_tool("variant_guidance", {
                        "variant_name": name, "printer": "P2S", "nozzle_mm": 0.4,
                        "plate": "Textured PEI", "material": "PLA", "intended_use": "desk-organization",
                    })
                    assert json.loads(result.content[0].text)["status"] == "suggested_starting_points"
                    result = await session.call_tool("create_variant", {
                        "template_id": "rounded-organizer", "variant_name": name + "-bad",
                        "parameters": {"compartments": True},
                    })
                    assert result.isError
                finally:
                    if output.is_dir():
                        shutil.rmtree(output)
                        render_index(output.parent)
    print("MCP stdio: discovery, metadata, checked customization, local export and invalid-input rejection passed.")


if __name__ == "__main__":
    asyncio.run(check())
