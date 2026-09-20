from .db import SessionLocal
from .models import Employee

db = SessionLocal()

employees = [
    Employee(name="Rahul", email="rahul@kohler.com", designation="Employee"),
    Employee(name="Priya", email="priya@kohler.com", designation="Manager"),
    Employee(name="Arjun", email="arjun@kohler.com", designation="Finance Admin"),
    Employee(name="Mukund", email="mukund@kohler.com", designation="GM"),
]

db.add_all(employees)
db.commit()
db.close()

print("Sample employees added.")