from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pwdlib import PasswordHash

from backend.database.db import SessionLocal
from backend.database.models import Employee
from backend.auth.auth import create_access_token


router = APIRouter()

password_hash = PasswordHash.recommended()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(credentials: LoginRequest):

    db = SessionLocal()

    try:
        employee = (
            db.query(Employee)
            .filter(Employee.email == credentials.email)
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not employee.password_hash:
            raise HTTPException(
                status_code=401,
                detail="Password not configured for this account"
            )

        if not password_hash.verify(
            credentials.password,
            employee.password_hash
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        token = create_access_token(
            employee.id,
            employee.designation
        )

        return {
            "access_token": token,
            "employee": employee.name,
            "designation": employee.designation
        }

    finally:
        db.close()