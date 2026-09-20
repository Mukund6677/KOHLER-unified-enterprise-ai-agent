from backend.agents.intent import (
    detect_department,
    detect_action
)


tests = [
    "Show me the financial reports",
    "How many hydraulic pumps are available?",
    "Show me employee leave information",
    "Change inventory to 700 units"
]


for query in tests:

    print("\nQuery:", query)

    print(
        "Department:",
        detect_department(query)
    )

    print(
        "Action:",
        detect_action(query)
    )