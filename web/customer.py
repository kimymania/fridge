from typing import Annotated

from fastapi import APIRouter, Body

from model.customer import Customer
from service import customer as service

router = APIRouter(prefix="/customer")


@router.get("/")
def get_all():
    return service.get_all()


@router.post("/")
def create_customer(
    name: Annotated[str, Body(...)],
    address: Annotated[str, Body(...)],
    phone: Annotated[str, Body(...)],
    email: Annotated[str, Body(...)],
):
    customer = Customer(name=name, address=address, phone=phone, email=email)
    return service.create_customer(customer)
