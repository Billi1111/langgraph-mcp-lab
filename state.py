from typing import Any, NotRequired, TypedDict

class AgentState(TypedDict):

    national_id: str

    validation_result: NotRequired[dict[str, str]]

    envelope: NotRequired[dict[str, Any]]

    #shared memory between graph nodes
