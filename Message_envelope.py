from dataclasses import asdict, dataclass
from typing import Any


PROTOCOL_VERSION = "1.0"

@dataclass
class MessageEnvelope:
    sender_agent_id: str
    receiver_agent_id: str
    task: str
    artifact_refs: list[str]
    trust_context: dict[str, Any]
    protocol_version: str

    def __post_init__(self) -> None:
        if self.protocol_version != PROTOCOL_VERSION:
            raise ValueError(
                f"Unsupported protocol version: {self.protocol_version}"
            )

        for name in ("sender_agent_id", "receiver_agent_id", "task"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")
        if not isinstance(self.artifact_refs, list) or not all(
            isinstance(ref, str) and ref.strip() for ref in self.artifact_refs
        ):
            raise ValueError("artifact_refs must be a list of non-empty strings")
        if not isinstance(self.trust_context, dict):
            raise ValueError("trust_context must be an object")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MessageEnvelope":
        """Validate a received envelope, including its application version."""
        return cls(**data)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
 
