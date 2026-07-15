from .state import GraphState


def member1_node(state: GraphState):
    print("=" * 50)
    print("Running Member 1 - Document processing")
    print("=" * 50)

    state["member1_output"] = {
        "document_id": "doc_001",
        "chunks": [
            {
                "chunk_id": "chunk_1",
                "text": "Payment must be completed within 30 days."
            },
            {
                "chunk_id": "chunk_2",
                "text": "Agreement automatically renews every year."
            },
            {
                "chunk_id": "chunk_3",
                "text": "Either party may terminate with 60 days notice."
            }
        ]
    }

    state["current_node"] = "Member 1 Completed"

    return state


def member2_node(state: GraphState):
    print("=" * 50)
    print("Running Member 2 - Contract Analysis")
    print("=" * 50)

    state["member2_output"] = {
        "clauses": {
            "payment": {
                "found": True,
                "text": "Payment within 30 days."
            },
            "renewal": {
                "found": True,
                "text": "Automatically renews yearly."
            },
            "termination": {
                "found": True,
                "text": "60 day notice."
            }
        }
    }

    state["current_node"] = "Member 2 Completed"

    return state


def member3_node(state: GraphState):
    print("=" * 50)
    print("Running Member 3 - Risk Assessment")
    print("=" * 50)

    state["member3_output"] = {
        "summary": "This contract contains payment, renewal and termination clauses.",
        "risk_score": 72,
        "risk_level": "Medium",
        "risks": [
            "Automatic renewal",
            "Long termination notice"
        ],
        "answer": "The contract is moderately risky because it automatically renews unless cancelled."
    }

    state["final_output"] = state["member3_output"]

    state["current_node"] = "Member 3 Completed"

    return state
