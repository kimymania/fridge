from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from model.customer import Customer
from service import customer as service

router = APIRouter(prefix="/html")

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def get_all(request: Request):
    customers = service.get_all()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "customers": customers,
        },
    )


@router.post("/", response_class=HTMLResponse)
def create(
    request: Request,
    name: Annotated[str, Form(...)],
    address: Annotated[str, Form(...)],
    phone: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
):
    service.create_customer(
        Customer(
            name=name,
            address=address,
            phone=phone,
            email=email,
        )
    )
    return RedirectResponse("/html", status_code=302)


@router.post("/update", response_class=HTMLResponse)
def modify_customer(
    request: Request,
    original_name: Annotated[str, Form(...)],
    name: Annotated[str, Form(...)],
    address: Annotated[str, Form(...)],
    phone: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
):
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
