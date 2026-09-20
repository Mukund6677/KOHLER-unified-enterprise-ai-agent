from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.audit.audit_log import log_action
from jose import jwt, JWTError
from backend.actions.finance_action import execute_finance_modification
from backend.database.db import engine, Base
from backend.database.models import Employee
from backend.auth.login import router as auth_router
from backend.auth.permissions import has_permission
from backend.rag.secure_search import secure_search
from backend.hitl.approval import create_approval, approve_request
from backend.agents.orchestrator import orchestrate
from backend.auth.auth import SECRET_KEY, ALGORITHM
from backend.auth.auth import get_current_user

# Authentication
security = HTTPBearer()


app = FastAPI(title="KOHLER Unified Enterprise AI Agent")
# CORS - allows React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "KOHLER AI Agent is running"}


@app.get("/employees")
def get_employees(current_user: dict = Depends(get_current_user)):
    from backend.database.db import SessionLocal

    db = SessionLocal()
    employees = db.query(Employee).all()

    result = [
        {
            "id": e.id,
            "name": e.name,
            "email": e.email,
            "designation": e.designation
        }
        for e in employees
    ]

    db.close()
    return result


# Authentication
app.include_router(auth_router, prefix="/auth")


# Permission checking
@app.get("/check-permission")
def check_permission(designation: str, permission: str, current_user: dict = Depends(get_current_user)):
    return {
        "designation": designation,
        "permission": permission,
        "allowed": has_permission(designation, permission)
    }


# Secure RAG
@app.get("/secure-search")
def secure_search_endpoint(
    query: str,
    current_user: dict = Depends(get_current_user)
):
    employee_id = current_user["employee_id"]
    designation = current_user["designation"]

    result = orchestrate(
        query,
        designation,
        employee_id
    )

    return result


# HITL approval
@app.post("/approval/request")
def request_approval(employee: str, action: str, details: str, current_user: dict = Depends(get_current_user)):
    return create_approval(employee, action, details)


@app.post("/approval/approve")
def approve(
    request_id: int,
    current_user: dict = Depends(get_current_user)
):
    approver = current_user["employee_id"]
    designation = current_user["designation"]

    if designation != "GM":
        raise HTTPException(
            status_code=403,
            detail="Only GM can approve requests."
        )

    result = approve_request(
        request_id,
        approver
    )

    if result.get("status") == "APPROVED":

        action = result.get("action")

        # -----------------------------
        # Finance execution
        # -----------------------------

        if action == "FINANCE_MODIFICATION":

            execution = execute_finance_modification(
                employee=result["employee"],
                details=result["details"],
                approved_by=approver
            )

        # -----------------------------
        # Operations execution
        # -----------------------------

        elif action == "OPERATIONS_MODIFICATION":

            from backend.actions.operations_action import (
                execute_operations_modification
            )

            execution = execute_operations_modification(
                employee=result["employee"],
                details=result["details"],
                approved_by=approver
            )

        else:

            return {
                "error": "Unknown approval action."
            }

        result["execution"] = execution

        # -----------------------------
        # Audit
        # -----------------------------

        audit = log_action(
            employee=result["employee"],
            action=result["action"],
            details=result["details"],
            approved_by=approver,
            status=execution["status"]
        )

        result["audit_log"] = audit

    return result

@app.get("/audit/logs")
def get_audit_logs(
    current_user: dict = Depends(get_current_user)
):
    designation = current_user["designation"]

    if designation != "GM":
        raise HTTPException(
            status_code=403,
            detail="Only GM can view audit logs."
        )

    from backend.audit.audit_log import get_audit_logs as fetch_audit_logs

    return {
        "logs": fetch_audit_logs()
    }

@app.get("/approval/pending")
def pending_approvals(
    current_user: dict = Depends(get_current_user)
):
    designation = current_user["designation"]

    if designation != "GM":
        raise HTTPException(
            status_code=403,
            detail="Only GM can view approval requests."
        )

    from backend.hitl.approval import get_pending_approvals

    return {
        "approvals": get_pending_approvals()
    }