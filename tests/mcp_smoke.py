"""Exercise the real optional SDK over stdio, including export and rejection."""

import asyncio
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from tools.catalog import ROOT, build_model


async def check():
    server = StdioServerParameters(command=sys.executable, args=["-m", "tools.mcp_server"], cwd=str(ROOT))
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert {tool.name for tool in tools.tools} == {"list_models", "describe_model", "check_model", "export_model"}
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
    print("MCP stdio: discovery, metadata, checked customization, local export and invalid-input rejection passed.")


if __name__ == "__main__":
    asyncio.run(check())
