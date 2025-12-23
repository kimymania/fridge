from data import fridge
from model.fridge import Food


def get_all(user):
    return fridge.get_all(user)


def add_food(food: Food, user):
    return fridge.add_food(food, user)


def update_food_quantity(food: Food, user):
    return fridge.update_food_quantity(food, user)


def remove_food(food_name: str, user):
    return fridge.remove_food(food_name, user)
