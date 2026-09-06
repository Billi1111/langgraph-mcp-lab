from langgraph.graph import END, START, StateGraph

from nodes import envelope_node, ingest_node, validate_node
from state import AgentState


def build_graph():
	graph = StateGraph(AgentState)
	graph.add_node("ingest", ingest_node)
	graph.add_node("validate", validate_node)
	graph.add_node("envelope", envelope_node)
	graph.add_edge(START, "ingest")
	graph.add_edge("ingest", "validate")
	graph.add_edge("validate", "envelope")
	graph.add_edge("envelope", END)
	return graph.compile()
