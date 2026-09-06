from Message_envelope import MessageEnvelope, PROTOCOL_VERSION
from mcp_tool import MCPToolConnector
from state import AgentState


connector = MCPToolConnector()


def ingest_node(state: AgentState) -> dict[str, str]:
    national_id = state["national_id"]
    if not isinstance(national_id, str):
        raise TypeError("national_id must be a string")
    return {"national_id": national_id.strip()}


async def validate_node(state: AgentState) -> dict[str, dict[str, str]]:
    result = await connector.call(
        "validate_national_id",
        {"national_id": state["national_id"]},
    )
    if (
        result.get("status") not in ("valid", "invalid")
        or result.get("national_id") != state["national_id"]
    ):
        raise ValueError("Unexpected validation result from MCP server")
    return {"validation_result": result}


def envelope_node(state: AgentState) -> dict[str, dict]:
    envelope = MessageEnvelope(
        sender_agent_id="national-id-agent",
        receiver_agent_id="result-consumer",
        task="validate_national_id",
        artifact_refs=["validation_result"],
        trust_context={
            "source": "mcp", "tool": "validate_national_id",
            "transport": "stdio", "validation_scope": "format_only",
        },
        protocol_version=PROTOCOL_VERSION,
    )
    return {"envelope": envelope.to_dict()}
