from data import my_food
from model.my_food import Food


def get_all():
    return my_food.get_all()


def add_food(food: Food):
    return my_food.add_food(food)


def update_food_quantity(food: Food):
    return my_food.update_food_quantity(food)


def remove_food(food_name: str):
    return my_food.remove_food(food_name)
