from datetime import datetime

from backend.database.db import SessionLocal
from backend.database.enterprise_models import AuditRecord


def log_action(
    employee,
    action,
    details,
    approved_by=None,
    status="SUCCESS",
    agent=None,
    department=None
):
    db = SessionLocal()

    try:
        record = AuditRecord(
            employee_id=employee,
            agent=agent,
            department=department,
            action=action,
            details=details,
            approved_by=approved_by,
            status=status,
            timestamp=datetime.utcnow()
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.id,
            "timestamp": (
                record.timestamp.isoformat()
                if record.timestamp
                else None
            ),
            "employee": record.employee_id,
            "agent": record.agent,
            "department": record.department,
            "action": record.action,
            "details": record.details,
            "approved_by": record.approved_by,
            "status": record.status
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_audit_logs():
    db = SessionLocal()

    try:
        records = (
            db.query(AuditRecord)
            .order_by(
                AuditRecord.timestamp.desc()
            )
            .all()
        )

        return [
            {
                "id": record.id,
                "timestamp": (
                    record.timestamp.isoformat()
                    if record.timestamp
                    else None
                ),
                "employee": record.employee_id,
                "agent": record.agent,
                "department": record.department,
                "action": record.action,
                "details": record.details,
                "approved_by": record.approved_by,
                "status": record.status
            }
            for record in records
        ]

    finally:
        db.close()