from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text
from datetime import datetime

from backend.database.db import Base
from backend.database.models import Employee


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String, unique=True, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String, nullable=False, default="units")
    reorder_level = Column(Integer, nullable=False, default=0)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    supplied_item = Column(String, nullable=False)
    contact_email = Column(String)
    status = Column(String, nullable=False, default="Active")


class FinanceRecord(Base):
    __tablename__ = "finance_records"

    id = Column(Integer, primary_key=True, index=True)
    record_type = Column(String, nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="INR")
    status = Column(String, nullable=False, default="Approved")
    description = Column(Text)


class HRRecord(Base):
    __tablename__ = "hr_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    record_type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    effective_date = Column(Date)
    status = Column(String, nullable=False, default="Active")
    notes = Column(Text)


class ApprovalRecord(Base):
    __tablename__ = "approval_records"

    id = Column(Integer, primary_key=True, index=True)
    requester_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    approver_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    action_type = Column(String, nullable=False)
    target_type = Column(String, nullable=False)
    target_id = Column(Integer, nullable=True)
    details = Column(Text, nullable=False)
    status = Column(String, nullable=False, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)


class AuditRecord(Base):
    __tablename__ = "audit_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    agent = Column(String)
    department = Column(String)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    approved_by = Column(Integer, ForeignKey("employees.id"), nullable=True)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
