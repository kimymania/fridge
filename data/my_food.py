from sqlite3 import IntegrityError

from error import Duplicate, Missing
from model.my_food import Food

from .init_db import create_db

conn, curs = create_db()
curs.execute("""CREATE TABLE IF NOT EXISTS refrigerator(
    food_name TEXT PRIMARY KEY,
    quantity INTEGER)
""")


def row_to_model(row: tuple[str, int]) -> Food:
    food_name, quantity = row
    return Food(food_name=food_name, quantity=quantity)


def model_to_dict(model: Food) -> dict:
    return model.model_dump()


def get_all() -> list[Food]:
    sql = """SELECT * FROM refrigerator"""
    curs.execute(sql)
    datas = curs.fetchall()
    return [row_to_model(data) for data in datas]


def add_food(food: Food):
    sql = """INSERT INTO refrigerator (food_name, quantity) VALUES (:food_name, :quantity)"""
    params = model_to_dict(food)
    try:
        curs.execute(sql, params)
    except IntegrityError as e:
        raise Duplicate(f"{food.food_name} is already in the fridge: {e}")
    conn.commit()


def update_food_quantity(food: Food):
    sql = """UPDATE refrigerator SET quantity=:quantity WHERE food_name=:food_name"""
    params = model_to_dict(food)
    curs.execute(sql, params)
    if curs.rowcount == 1:
        conn.commit()
    else:
        raise Missing(f"{food.food_name} not found")


def remove_food(food_name: str):
    sql = """DELETE FROM refrigerator WHERE food_name=:food_name"""
    params = {"food_name": food_name}
    curs.execute(sql, params)
    if curs.rowcount != 1:
        raise Missing(f"{food_name} not found")
    conn.commit()
