import uvicorn
from fastapi import FastAPI

from web import fridge, login, user

app = FastAPI()

app.include_router(user.router)
app.include_router(fridge.router)
app.include_router(login.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
