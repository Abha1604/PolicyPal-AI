from typing import TypedDict, Dict, Any


class GraphState(TypedDict):
    pdf_path: str
    question: str

    member1_output: Dict[str, Any]
    member2_output: Dict[str, Any]
    member3_output: Dict[str, Any]

    current_node: str

    retrieved_clause: Dict[str, Any]
    qa_output: Dict[str, Any]

    final_output: Dict[str, Any]
