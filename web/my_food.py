from fastapi import APIRouter, Body, HTTPException, status

from error import Duplicate, Missing
from model.my_food import Food
from service import my_food

router = APIRouter(prefix="/myfood")


@router.get("/")
def get_all():
    return my_food.get_all()


@router.post("/")
def add_food(food: Food):
    if food.quantity < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food quantity needs to be higher than 0",
        )
    try:
        return my_food.add_food(food)
    except Duplicate as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)


@router.put("/")
def update_food_quantity(food: Food):
    try:
        return my_food.update_food_quantity(food)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)


@router.delete("/")
def remove_food(food_name=Body(embed=True)):
    try:
        return my_food.remove_food(food_name)
    except Missing as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.msg)
