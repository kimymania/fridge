import uvicorn
from fastapi import FastAPI

from web import my_food

app = FastAPI()

app.include_router(my_food.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
