from backend.rag.secure_search import secure_search

print("EMPLOYEE:")
print(secure_search(
    "Who can access confidential financial information?",
    "Employee"
))

print("\nGM:")
print(secure_search(
    "Who can access confidential financial information?",
    "GM"
))