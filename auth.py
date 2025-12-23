from datetime import datetime, timedelta
from typing import Any

import bcrypt
from fastapi import HTTPException
from jose import jwt

from data import user as data
from model.user import User

SECRET_KEY = "9A2D253F008E9667ECE093F3C427CC8689107B3299172E3C5DE0DF65AA24125E"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def unauth():
    raise HTTPException(
        status_code=404,
        detail="Wrong credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(user: User):
    data: dict[str, Any] = {"sub": user.name}
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.now()
    data.update({"exp": now + expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    if not (username := payload.get("sub")):
        return None
    return username


def find_user(username) -> User | None:
    if user := data.find_user(username):
        return user
    return None


def verify_password(password: str, hashed_password: str) -> bool:
    encoded_password = password.encode("utf-8")
    encoded_hashed_password = hashed_password.encode("utf-8")
    is_valid = bcrypt.checkpw(encoded_password, encoded_hashed_password)
    return is_valid


def hash_password(password: str) -> str:
    encoded_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    return hashed_password.decode("utf-8")


def get_current_user(token: str):
    """Decode token -> check if user in DB

    :returns: username string"""
    username = decode_token(token)
    user = find_user(username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="올바르지 않은 인증정보입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.name
