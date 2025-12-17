from datetime import datetime, timedelta

import bcrypt
from jose import jwt

from data import user as data
from model.user import DB_User, User

SECRET_KEY = "9A2D253F008E9667ECE093F3C427CC8689107B3299172E3C5DE0DF65AA24125E"
ALGORITHM = "HS256"


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


# post token
def auth_user(username, password) -> User | None:
    user = find_user(username)
    if not user:
        return None
    password_check = verify_password(password, user.hashed_password)
    if not password_check:
        return None
    return user


def create_access_token(data: dict, expire: timedelta):
    data = data.copy()
    now = datetime.now()
    data.update({"exp": now + expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_user(user: DB_User):
    user = DB_User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.hashed_password),
    )
    return data.create_user(user)
