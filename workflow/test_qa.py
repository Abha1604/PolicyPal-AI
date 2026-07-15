from .qa_graph import qa_app

initial_state = {
    "pdf_path": "contracts/sample.pdf",
    "question": "Can I terminate this contract?",

    "member1_output": {},
    "member2_output": {},
    "member3_output": {},

    "current_node": "",

    "retrieved_clause": {},
    "qa_output": {},
    "final_output": {}
}

result = qa_app.invoke(initial_state)

print("\n===== Q&A OUTPUT =====\n")
print(result["qa_output"])
