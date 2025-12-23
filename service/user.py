from auth import find_user, hash_password, verify_password
from data import user as data
from model.user import DB_User, User


def create_user(username: str, password: str):
    user = DB_User(
        name=username,
        hashed_password=hash_password(password),
    )
    return data.create_user(user)


def auth_user(username, password) -> User | None:
    user = find_user(username)
    if not user:
        return None
    password_check = verify_password(password, user.hashed_password)
    if not password_check:
        return None
    return user
