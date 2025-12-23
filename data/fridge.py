from sqlite3 import IntegrityError

from error import Duplicate, Missing
from model.fridge import Food

from .init_db import create_db

conn, curs = create_db()


def row_to_model(row: tuple[str, int]) -> Food:
    food_name, quantity = row
    return Food(food_name=food_name, quantity=quantity)


def model_to_dict(model: Food) -> dict:
    return model.model_dump()


def get_all(user: str) -> list[Food]:
    sql = """SELECT food_name, quantity FROM refrigerator WHERE user = :user"""
    params = {"user": user}
    curs.execute(sql, params)
    datas = curs.fetchall()
    return [row_to_model(data) for data in datas]


def add_food(food: Food, user: str):
    sql = """INSERT INTO refrigerator (food_name, quantity, user) VALUES (:food_name, :quantity, :user)"""
    params = model_to_dict(food)
    params["user"] = user
    try:
        curs.execute(sql, params)
    except IntegrityError as e:
        raise Duplicate(f"{food.food_name} is already in the fridge: {e}")
    conn.commit()


def update_food_quantity(food: Food, user: str):
    sql = """UPDATE refrigerator SET quantity=:quantity WHERE food_name=:food_name AND user=:user"""
    params = model_to_dict(food)
    params["user"] = user
    curs.execute(sql, params)
    if curs.rowcount == 1:
        conn.commit()
    else:
        raise Missing(f"{food.food_name} not found")


def remove_food(food_name: str, user):
    sql = """DELETE FROM refrigerator WHERE food_name=:food_name AND user=:user"""
    params = {
        "food_name": food_name,
        "user": user,
    }
    curs.execute(sql, params)
    if curs.rowcount != 1:
        raise Missing(f"{food_name} not found")
    conn.commit()
