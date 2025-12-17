from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from error import Duplicate
from model.user import DB_User
from service import user as service

router = APIRouter(prefix="/user")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2 = OAuth2PasswordBearer(tokenUrl="/user/token")


def unauth():
    raise HTTPException(
        status_code=404,
        detail="Wrong credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token")
async def create_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauth()
    else:  # only here to satisfy linters thinking user might be None
        expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = service.create_access_token(
            data={"sub": user.name},
            expire=expire,
        )
        return {"access_token": access_token, "token_type": "bearer"}


@router.post("/")
async def create_user(user: DB_User):
    try:
        return service.create_user(user)
    except Duplicate as e:
        raise HTTPException(status_code=401, detail=e)


@router.get("/{username}")
def find_user(username):
    return service.find_user(username)
