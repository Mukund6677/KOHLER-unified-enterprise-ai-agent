from datetime import date
from pwdlib import PasswordHash
from backend.database.db import Base, engine, SessionLocal
from backend.database.models import Employee
from backend.database.enterprise_models import (
    Department,
    Supplier,
    InventoryItem,
    FinanceRecord,
    HRRecord,
    ApprovalRecord,
    AuditRecord,
)

# Create all enterprise tables while preserving the existing Employee table.
Base.metadata.create_all(bind=engine)

db = SessionLocal()
password_hash = PasswordHash.recommended()

try:
    # -------------------------
    # Departments
    # -------------------------
    departments = [
        ("HR", "Human Resources and employee management"),
        ("Finance", "Financial planning, reporting and controls"),
        ("Operations", "Production, inventory and suppliers"),
        ("Engineering", "Engineering and product development"),
        ("IT", "Technology and enterprise systems"),
    ]

    for name, description in departments:
        if not db.query(Department).filter_by(name=name).first():
            db.add(Department(name=name, description=description))

    db.commit()

    # -------------------------
    # Existing demo users
    # -------------------------
    demo_users = [
        ("Rahul", "rahul@kohler.com", "Rahul@2026!", "Employee"),
        ("Priya", "priya@kohler.com", "Priya@2026!", "Manager"),
        ("Arjun", "arjun@kohler.com", "Arjun@2026!", "Finance Admin"),
        ("Mukund", "mukund@kohler.com", "Mukund@2026!", "GM"),
        ("Operations Admin", "operations_admin@kohler.com", "OpsAdmin@2026!", "Operations Admin"),
        ("Neha", "neha@kohler.com", "Neha@2026!", "HR Admin"),
        ("Vikram", "vikram@kohler.com", "Vikram@2026!", "Operations Manager"),
        ("Aisha", "aisha@kohler.com", "Aisha@2026!", "Employee"),
        ("Rohan", "rohan@kohler.com", "Rohan@2026!", "Employee"),
        ("Sneha", "sneha@kohler.com", "Sneha@2026!", "Employee"),
        ("Karan", "karan@kohler.com", "Karan@2026!", "Employee"),
        ("Meera", "meera@kohler.com", "Meera@2026!", "Manager"),
    ]

    for name, email, password, designation in demo_users:
        employee = db.query(Employee).filter_by(email=email).first()

        if not employee:
            db.add(Employee(
                name=name,
                email=email,
                password_hash=password_hash.hash(password),
                designation=designation,
            ))

    db.commit()

    # Refresh employee lookup after inserts.
    employees = {
        e.email: e
        for e in db.query(Employee).all()
    }

    # -------------------------
    # Suppliers
    # -------------------------
    suppliers = [
        ("Supplier Alpha", "Hydraulic Pumps", "alpha@kohler-demo.com"),
        ("Supplier Beta", "Industrial Valves", "beta@kohler-demo.com"),
        ("Supplier Gamma", "Motor Assemblies", "gamma@kohler-demo.com"),
        ("Supplier Delta", "Control Modules", "delta@kohler-demo.com"),
    ]

    for name, item, email in suppliers:
        if not db.query(Supplier).filter_by(name=name).first():
            db.add(Supplier(
                name=name,
                supplied_item=item,
                contact_email=email,
                status="Active",
            ))

    db.commit()

    supplier_map = {
        s.name: s
        for s in db.query(Supplier).all()
    }

    # -------------------------
    # Inventory
    # -------------------------
    inventory = [
        ("Hydraulic Pumps", "Industrial Components", 420, "units", 150, "Supplier Alpha"),
        ("Industrial Valves", "Industrial Components", 275, "units", 100, "Supplier Beta"),
        ("Motor Assemblies", "Industrial Components", 180, "units", 75, "Supplier Gamma"),
        ("Control Modules", "Electronic Components", 350, "units", 120, "Supplier Delta"),
        ("Pressure Sensors", "Sensors", 240, "units", 80, "Supplier Alpha"),
        ("Flow Controllers", "Control Systems", 125, "units", 50, "Supplier Beta"),
    ]

    for item_name, category, quantity, unit, reorder, supplier_name in inventory:
        existing = db.query(InventoryItem).filter_by(item_name=item_name).first()
        if not existing:
            db.add(InventoryItem(
                item_name=item_name,
                category=category,
                quantity=quantity,
                unit=unit,
                reorder_level=reorder,
                supplier_id=supplier_map[supplier_name].id,
            ))

    db.commit()

    # -------------------------
    # Finance records
    # -------------------------
    finance = [
        ("Revenue", 2026, "Company", 125000000.0, "INR", "Approved", "Synthetic FY2026 company revenue"),
        ("Budget", 2026, "Operations", 32000000.0, "INR", "Approved", "Synthetic FY2026 operations budget"),
        ("Budget", 2026, "HR", 8500000.0, "INR", "Approved", "Synthetic FY2026 HR budget"),
        ("Budget", 2026, "Finance", 6000000.0, "INR", "Approved", "Synthetic FY2026 finance budget"),
        ("Expense", 2026, "Operations", 18750000.0, "INR", "Approved", "Synthetic operations expenses"),
        ("Expense", 2026, "HR", 4200000.0, "INR", "Approved", "Synthetic HR expenses"),
        ("Profit", 2026, "Company", 28750000.0, "INR", "Approved", "Synthetic FY2026 operating profit"),
    ]

    if db.query(FinanceRecord).count() == 0:
        for row in finance:
            db.add(FinanceRecord(
                record_type=row[0],
                fiscal_year=row[1],
                department=row[2],
                amount=row[3],
                currency=row[4],
                status=row[5],
                description=row[6],
            ))

    db.commit()

    # -------------------------
    # HR records
    # -------------------------
    hr_seed = [
        ("rahul@kohler.com", "leave_balance", "18 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("priya@kohler.com", "leave_balance", "16 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("arjun@kohler.com", "leave_balance", "20 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("mukund@kohler.com", "leave_balance", "22 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("neha@kohler.com", "leave_balance", "19 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("vikram@kohler.com", "leave_balance", "17 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("aisha@kohler.com", "leave_balance", "21 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("rohan@kohler.com", "leave_balance", "15 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("sneha@kohler.com", "leave_balance", "20 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("karan@kohler.com", "leave_balance", "14 paid leave days remaining", date(2026, 1, 1), "Active"),
        ("meera@kohler.com", "leave_balance", "18 paid leave days remaining", date(2026, 1, 1), "Active"),
    ]

    if db.query(HRRecord).count() == 0:
        for email, record_type, value, effective_date, status in hr_seed:
            employee = employees.get(email)
            if employee:
                db.add(HRRecord(
                    employee_id=employee.id,
                    record_type=record_type,
                    value=value,
                    effective_date=effective_date,
                    status=status,
                ))

    db.commit()

    print("Synthetic enterprise database initialized successfully.")
    print(f"Employees: {db.query(Employee).count()}")
    print(f"Departments: {db.query(Department).count()}")
    print(f"Inventory items: {db.query(InventoryItem).count()}")
    print(f"Finance records: {db.query(FinanceRecord).count()}")
    print(f"HR records: {db.query(HRRecord).count()}")
    print(f"Suppliers: {db.query(Supplier).count()}")

finally:
    db.close()
