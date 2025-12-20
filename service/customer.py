from data import customer as data
from model.customer import Customer


def get_all():
    return data.get_all()


def create_customer(customer: Customer):
    return data.create_customer(customer)


def update_customer(customer_name: str, updated_customer: Customer):
    return data.update_customer(customer_name, updated_customer)
