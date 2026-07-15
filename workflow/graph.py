from langgraph.graph import StateGraph, END

from .state import GraphState
from .nodes import member1_node, member2_node, member3_node

# Create the graph
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("member1", member1_node)
workflow.add_node("member2", member2_node)
workflow.add_node("member3", member3_node)

# Define flow
workflow.set_entry_point("member1")

workflow.add_edge("member1", "member2")
workflow.add_edge("member2", "member3")
workflow.add_edge("member3", END)

# Compile graph
app = workflow.compile()
