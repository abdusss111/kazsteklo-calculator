import os, jwt
from typing import Optional
from data.google_client import get_spreadsheet
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")  # put this in your .env!
JWT_EXP_HOURS = int(os.getenv("JWT_EXP_HOURS", 24))


def get_users_from_sheet() -> list[dict]:
    sheet = get_spreadsheet().worksheet("пользователи")
    rows = sheet.get_all_values()[1:]  # Skip header row
    users = []

    for row in rows:
        if len(row) >= 3:
            username = row[1].strip()
            password = row[2].strip()
            users.append({"username": username, "password": password})

    return users


def validate_credentials(username: str, password: str) -> bool:
    users = get_users_from_sheet()
    return any(u["username"] == username and u["password"] == password for u in users)


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXP_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.PyJWTError:
        return None


security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )