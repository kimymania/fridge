import bcrypt
from fastapi import HTTPException
from jose import jwt

from data import user as data
from model.user import DB_User, User


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


def create_user(username: str, password: str):
    user = DB_User(
        name=username,
        hashed_password=hash_password(password),
    )
    return data.create_user(user)


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    if not (username := payload.get("sub")):
        return None
    return username


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


def check_usable(token: str):
    username = get_current_user(token)
    if _fake_db[username]:
        return True
    return False


def check_user(token: str):
    check = check_usable(token)
    return check
