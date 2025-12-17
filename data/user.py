from model.user import DB_User, User

from .init_db import curs

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
