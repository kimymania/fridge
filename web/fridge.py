from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from auth import get_current_user, unauth
from model.fridge import Food
from service import fridge as service
from service import user as user

router = APIRouter(prefix="/fridge", tags=["fridge"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def get_all(request: Request):
    token = request.cookies["token"]
    username = get_current_user(token)
    if username:
        items = service.get_all(username)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "username": username,
                "items": items,
            },
        )
    else:
        unauth()


@router.post("/", response_class=HTMLResponse)
def add_food(
    request: Request,
    food_name: Annotated[str, Form(...)],
    quantity: Annotated[int, Form(...)],
):
    token = request.cookies["token"]
    if username := get_current_user(token):
        service.add_food(
            Food(
                food_name=food_name,
                quantity=quantity,
            ),
            username,
        )
        return RedirectResponse("/fridge", status_code=302)
    else:
        unauth()


@router.post("/update", response_class=HTMLResponse)
def update_food_quantity(
    request: Request,
    food_name: Annotated[str, Form(...)],
    quantity: Annotated[int, Form(...)],
):
    token = request.cookies["token"]
    if username := get_current_user(token):
        service.update_food_quantity(
            Food(
                food_name=food_name,
                quantity=quantity,
            ),
            username,
        )
        return RedirectResponse("/fridge", status_code=302)
    else:
        unauth()


@router.post("/remove", response_class=HTMLResponse)
def remove_food(
    request: Request,
    food_name: Annotated[str, Form(...)],
):
    token = request.cookies["token"]
    if username := get_current_user(token):
        service.remove_food(food_name, username)
        return RedirectResponse("/fridge", status_code=302)
    else:
        unauth()
