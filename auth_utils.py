# auth_utils.py
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets
from datetime import datetime, timezone, timedelta

def generate_reset_token():
    return secrets.token_urlsafe(32)

def token_expiry_time():
    return datetime.now() + timedelta(minutes=30)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


ph = PasswordHasher()  # Argon2id with safe defaults


def hash_password(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password too short")
    if len(password) > 128:
        raise ValueError("Password too long")
    return ph.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)