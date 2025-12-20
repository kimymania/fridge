import uvicorn
from fastapi import FastAPI

from web import my_food, user

app = FastAPI()

app.include_router(my_food.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
