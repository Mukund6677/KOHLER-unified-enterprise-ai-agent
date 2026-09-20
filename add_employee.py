from backend.database.db import SessionLocal
from backend.database.models import Employee

db = SessionLocal()

employee = Employee(
    name="Operations Admin",
    email="operations_admin@kohler.com",
    designation="Operations Admin"
)

db.add(employee)
db.commit()

print("Operations Admin added successfully.")

db.close()