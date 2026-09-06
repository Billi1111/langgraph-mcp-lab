import asyncio
from pathlib import Path
import sys
from typing import Any

from mcp import Client, StdioServerParameters


class NationalIDTool:

    def validate(self, national_id: str) -> dict[str, str]:

        if not isinstance(national_id, str):
            raise TypeError("national_id must be a string")
        # Format check only; this does not verify a person's identity.
        if len(national_id) == 14 and national_id.isascii() and national_id.isdigit():
            return {
                "status": "valid",
                "national_id": national_id
            }

        return {
            "status": "invalid",
            "national_id": national_id
        }


class MCPToolConnector:
    """Call a local MCP server over standard input/output."""

    def __init__(self) -> None:
        self.server = StdioServerParameters(
            command=sys.executable,
            args=[str(Path(__file__).with_name("mcp_server.py").resolve())],
        )

    async def call(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        # One connection per call keeps the lab simple; exit cleans up the server.
        async with asyncio.timeout(30):
            async with Client(self.server) as client:
                result = await client.call_tool(name, arguments)
        # Inspect after cleanup so application errors aren't wrapped by SDK task groups.
        if result.is_error:
            raise RuntimeError(f"MCP tool failed: {name}")
        if not isinstance(result.structured_content, dict):
            raise RuntimeError(f"MCP tool returned no structured object: {name}")
        return result.structured_content
