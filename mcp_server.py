"""Local tool server. stdout is reserved for MCP protocol messages."""
from mcp.server import MCPServer
from mcp_tool import NationalIDTool

server = MCPServer("national-id-lab")


@server.tool()
def validate_national_id(national_id: str) -> dict[str, str]:
    """Check for exactly 14 ASCII digits (toy format rule)."""
    return NationalIDTool().validate(national_id)


if __name__ == "__main__":
    server.run(transport="stdio")
