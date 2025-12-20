import uvicorn
from fastapi import FastAPI

from web import customer, html, my_food, user

app = FastAPI()

app.include_router(my_food.router)
app.include_router(customer.router)
app.include_router(user.router)
app.include_router(html.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
