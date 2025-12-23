from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from data.init_db import init_db
from web import fridge, login


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(fridge.router)
app.include_router(login.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
