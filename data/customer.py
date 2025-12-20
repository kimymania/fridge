from sqlite3 import IntegrityError

from error import Duplicate
from model.customer import Customer

from .init_db import create_db

conn, curs = create_db()
curs.execute("""
    CREATE TABLE IF NOT EXISTS customers(
    name TEXT PRIMARY KEY,
    address TEXT,
    phone TEXT,
    email TEXT)
""")


def row_to_model(row: tuple) -> Customer:
    name, address, phone, email = row
    return Customer(
        name=name,
        address=address,
        phone=phone,
        email=email,
    )


def model_to_dict(customer: Customer):
    return customer.model_dump()


def create_customer(customer: Customer):
    sql = "INSERT INTO customers (name, address, phone, email) VALUES (:name, :address, :phone, :email)"
    params = model_to_dict(customer)
    try:
        curs.execute(sql, params)
    except IntegrityError:
        raise Duplicate(msg="이미 회원 가입이 되어있습니다.")
    conn.commit()
    return None


def get_all():
    sql = "SELECT * FROM customers"
    curs.execute(sql)
    datas = curs.fetchall()
    return [row_to_model(data) for data in datas]


def update_customer(customer_name: str, updated_customer: Customer):
    sql = """
    UPDATE customers
    SET name = :name, address = :address, phone = :phone, email = :email
    WHERE name = :customer_name
    """
    params = model_to_dict(updated_customer)
    params["customer_name"] = customer_name
    try:
        curs.execute(sql, params)
    except IntegrityError:
        raise
    conn.commit()
    return None


def delete_customer(name: str):
    sql = "DELETE FROM customers WHERE name = :name"
    params = {"name": name}
    curs.execute(sql, params)
    conn.commit()
    return None
