import json
import unittest

from main import run_async
from Message_envelope import MessageEnvelope
from mcp_tool import MCPToolConnector, NationalIDTool


class FormatTests(unittest.TestCase):
    def test_format_cases(self):
        for value, expected in [
            ("12345678901234", "valid"), ("00000000000000", "valid"),
            ("123", "invalid"), ("", "invalid"),
            ("abcdefghijklmn", "invalid"), ("١٢٣٤٥٦٧٨٩٠١٢٣٤", "invalid"),
        ]:
            with self.subTest(value=value):
                self.assertEqual(NationalIDTool().validate(value)["status"], expected)


class EnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.data = dict(
            sender_agent_id="sender", receiver_agent_id="receiver", task="validate",
            artifact_refs=["validation_result"], trust_context={}, protocol_version="1.0",
        )

    def test_json_round_trip(self):
        envelope = MessageEnvelope.from_dict(self.data)
        received = MessageEnvelope.from_dict(json.loads(json.dumps(envelope.to_dict())))
        self.assertEqual(envelope, received)

    def test_reject_unsupported_version(self):
        self.data["protocol_version"] = "2.0"
        with self.assertRaisesRegex(ValueError, "Unsupported protocol"):
            MessageEnvelope.from_dict(self.data)

    def test_reject_malformed_fields(self):
        for field, value in [("task", ""), ("artifact_refs", "result"), ("trust_context", [])]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                MessageEnvelope.from_dict({**self.data, field: value})


class PipelineTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_mcp_pipeline(self):
        for value, expected in [(" 12345678901234 ", "valid"), ("abcdefghijklmn", "invalid")]:
            with self.subTest(value=value):
                result = await run_async(value)
                self.assertEqual(result["national_id"], value.strip())
                self.assertEqual(result["validation_result"]["status"], expected)
                envelope = MessageEnvelope.from_dict(result["envelope"])
                self.assertEqual(envelope.protocol_version, "1.0")
                self.assertEqual(envelope.trust_context["transport"], "stdio")
                for ref in envelope.artifact_refs:
                    self.assertIn(ref, result)

    async def test_unknown_tool(self):
        with self.assertRaisesRegex(RuntimeError, "MCP tool failed"):
            await MCPToolConnector().call("missing_tool", {})

    async def test_invalid_tool_arguments(self):
        with self.assertRaisesRegex(RuntimeError, "MCP tool failed"):
            await MCPToolConnector().call("validate_national_id", {})

    async def test_non_string_input(self):
        with self.assertRaisesRegex(TypeError, "must be a string"):
            await run_async(123)


if __name__ == "__main__":
    unittest.main()
