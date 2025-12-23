from data import fridge
from model.fridge import Food


def get_all():
    return fridge.get_all()


def add_food(food: Food):
    return fridge.add_food(food)


def update_food_quantity(food: Food):
    return fridge.update_food_quantity(food)


def remove_food(food_name: str):
    return fridge.remove_food(food_name)
