from .graph import app

# Initial input
initial_state = {
    "pdf_path": "contracts/sample.pdf",
    "question": "Explain risks",

    "member1_output": {},
    "member2_output": {},
    "member3_output": {},
    "final_output": {}
}

# Run the workflow
result = app.invoke(initial_state)

print("\n===== FINAL OUTPUT =====\n")
print("\nWorkflow Completed Successfully")
print("\nCurrent Node:", result["current_node"])

print("\nFinal Report")
print(result["final_output"])
