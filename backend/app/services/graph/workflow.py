from langgraph.graph import END, StateGraph
from app.services.graph.state import GraphState
from app.services.graph.nodes import retrieve_node, grade_docs_node, generate_node
from app.services.graph.edges import grade_hallucination

def compile_workflow():
    workflow = StateGraph(GraphState)

    # 1. Define nodes
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("grade_documents", grade_docs_node)
    workflow.add_node("generate", generate_node)

    # 2. Build explicit control flow
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    
    workflow.add_edge("generate", END)

    # Compile into executable
    return workflow.compile()
