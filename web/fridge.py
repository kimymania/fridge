from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from model.customer import Customer
from service import fridge as service
from service import user as user

router = APIRouter(prefix="/fridge")

templates = Jinja2Templates(directory="templates")


def unauth():
    raise HTTPException(
        status_code=404,
        detail="Wrong credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/", response_class=HTMLResponse)
def get_all(request: Request):
    token = request.cookies["token"]
    username = user.get_current_user(token)
    if username:
        items = service.get_all()
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
def create(
    request: Request,
    name: Annotated[str, Form(...)],
    address: Annotated[str, Form(...)],
    phone: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
):
    token = request.cookies["token"]
    if user.get_current_user(token):
        service.create_customer(
            Customer(
                name=name,
                address=address,
                phone=phone,
                email=email,
            )
        )
        return RedirectResponse("/fridge", status_code=302)
    else:
        unauth()


@router.post("/update", response_class=HTMLResponse)
def modify_customer(
    request: Request,
    original_name: Annotated[str, Form(...)],
    name: Annotated[str, Form(...)],
    address: Annotated[str, Form(...)],
    phone: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
):
    token = request.cookies["token"]
    if user.get_current_user(token):
        service.update_customer(
            original_name,
            Customer(
                name=name,
                address=address,
                phone=phone,
                email=email,
            ),
        )
        return RedirectResponse("/html", status_code=302)
    else:
        unauth()


@router.post("/delete", response_class=HTMLResponse)
def delete_customer(request: Request, name: Annotated[str, Form(...)]):
    token = request.cookies["token"]
    if user.get_current_user(token):
        service.delete_customer(name)
        return RedirectResponse("/html", status_code=302)
    else:
        unauth()
