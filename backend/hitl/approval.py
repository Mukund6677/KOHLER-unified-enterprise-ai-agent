from datetime import datetime

from backend.database.db import SessionLocal
from backend.database.enterprise_models import ApprovalRecord


def create_approval(employee, action, details):
    db = SessionLocal()

    try:
        request = ApprovalRecord(
            requester_employee_id=employee,
            action_type=action,
            target_type="ENTERPRISE_DATA",
            details=details,
            status="PENDING"
        )

        db.add(request)
        db.commit()
        db.refresh(request)

        return {
            "id": request.id,
            "employee": request.requester_employee_id,
            "action": request.action_type,
            "details": request.details,
            "status": request.status
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_pending_approvals():
    db = SessionLocal()

    try:
        requests = (
            db.query(ApprovalRecord)
            .filter(
                ApprovalRecord.status == "PENDING"
            )
            .order_by(
                ApprovalRecord.created_at.desc()
            )
            .all()
        )

        return [
            {
                "id": request.id,
                "employee": request.requester_employee_id,
                "action": request.action_type,
                "details": request.details,
                "status": request.status,
                "created_at": (
                    request.created_at.isoformat()
                    if request.created_at
                    else None
                )
            }
            for request in requests
        ]

    finally:
        db.close()


def approve_request(request_id, approver_employee_id):
    db = SessionLocal()

    try:
        request = (
            db.query(ApprovalRecord)
            .filter(
                ApprovalRecord.id == request_id
            )
            .first()
        )

        if not request:
            return {
                "error": "Approval request not found."
            }

        if request.status != "PENDING":
            return {
                "error": "Approval request has already been processed."
            }

        request.status = "APPROVED"
        request.approver_employee_id = approver_employee_id
        request.approved_at = datetime.utcnow()

        db.commit()
        db.refresh(request)

        return {
            "id": request.id,
            "employee": request.requester_employee_id,
            "action": request.action_type,
            "details": request.details,
            "status": request.status,
            "approved_by": request.approver_employee_id,
            "approved_at": (
                request.approved_at.isoformat()
                if request.approved_at
                else None
            )
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()