from backend.hitl.approval import create_approval, approve_request

request = create_approval(
    "Arjun",
    "Modify finance record",
    "Update Q3 financial data"
)

print("REQUEST:", request)

print("\nEmployee tries:")
print(approve_request(request["id"], "Employee"))

print("\nGM tries:")
print(approve_request(request["id"], "GM"))