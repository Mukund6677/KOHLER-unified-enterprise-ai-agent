import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt, JWTError

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

security = HTTPBearer()


def create_access_token(employee_id: int, designation: str):
    payload = {
        "employee_id": employee_id,
        "designation": designation,
        "exp": datetime.utcnow() + timedelta(hours=2),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        employee_id = payload.get("employee_id")
        designation = payload.get("designation")

        if employee_id is None or designation is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return {
            "employee_id": employee_id,
            "designation": designation
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired authentication token"
        )