from backend.agents.orchestrator import orchestrate


print(
    orchestrate(
        "How many paid leave days do employees get?",
        "Employee"
    )
)

print(
    orchestrate(
        "How many hydraulic pumps are in inventory?",
        "Operations Admin"
    )
)

print(
    orchestrate(
        "What financial information can I access?",
        "Finance Admin"
    )
)