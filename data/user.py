from sqlite3 import IntegrityError

from error import Duplicate
from model.user import DB_User, User

from .init_db import conn, curs

curs.execute("""
    CREATE TABLE IF NOT EXISTS user(name text primary_key, email text, hashed_password text)
    """)


def row_to_model(row: tuple) -> DB_User:
    name, email, hashed_password = row
    return DB_User(
        name=name,
        email=email,
        hashed_password=hashed_password,
    )


def model_to_dict(user: User | DB_User):
    return user.model_dump()


def find_user(username):
    sql = "SELECT * FROM user WHERE name = :name"
    params = {"name": username}
    curs.execute(sql, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    return row


def create_user(user: DB_User):
    sql = "INSERT INTO user (name, email, hashed_password) VALUES (:name, :email, :hashed_password)"
    params = model_to_dict(user)
    try:
        curs.execute(sql, params)
    except IntegrityError:
        Duplicate(msg="이미 회원 가입이 되어있습니다.")
    conn.commit()
    return None
