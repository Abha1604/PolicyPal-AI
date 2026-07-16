from langgraph.graph import StateGraph, END

from .state import GraphState
from .qa_nodes import retrieve_node, answer_node

# Create a new graph
qa_workflow = StateGraph(GraphState)

# Add nodes
qa_workflow.add_node("retrieve", retrieve_node)
qa_workflow.add_node("answer", answer_node)

# Define flow
qa_workflow.set_entry_point("retrieve")

qa_workflow.add_edge("retrieve", "answer")
qa_workflow.add_edge("answer", END)

# Compile graph
qa_app = qa_workflow.compile()
