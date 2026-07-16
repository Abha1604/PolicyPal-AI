from .state import GraphState


def retrieve_node(state: GraphState):
    print("=" * 50)
    print("Retrieving Relevant Clause")
    print("=" * 50)

    state["retrieved_clause"] = {
        "clause_type": "Termination",
        "text": "Either party may terminate the agreement with 60 days notice."
    }

    return state


def answer_node(state: GraphState):
    print("=" * 50)
    print("Generating Answer")
    print("=" * 50)

    question = state["question"]

    state["qa_output"] = {
        "question": question,
        "answer": "Yes. The contract allows either party to terminate with a 60-day notice period.",
        "source": state["retrieved_clause"]["text"]
    }

    return state
