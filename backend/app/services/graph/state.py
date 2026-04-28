from typing import List, TypedDict

class GraphState(TypedDict):
    """
    Represents the internal state of our self-reflective LangGraph workflow.
    """
    query: str
    documents: list
    generation: str
    hallucination_retries: int
