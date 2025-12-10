import uvicorn
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter(prefix="/user")
oauth2 = OAuth2PasswordBearer(tokenUrl="token")


# Models
class User(BaseModel):
    name: str
    email: str


class DB_User(User):
    password: str


# Dummy data
fake_user_db = {
    "sponge": {
        "name": "sponge",
        "email": "sponge@gmail.com",
        "password": "hashed_1234",
        "active": False,
    },
    "bob": {
        "name": "bob",
        "email": "bob@gmail.com",
        "password": "hashed_2345",
        "active": True,
    },
}


def fake_hash_password(password: str):
    return "hashed_" + password


# Check user credentials
@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_user_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Enter correct email and password")

    h_password = fake_hash_password(form_data.password)
    if h_password != user_dict["password"]:
        raise HTTPException(status_code=400, detail="Enter correct email and password")

    return {"access_token": user_dict["name"], "token-type": "bearer"}


def get_user(db, username: str):
    user_db = db[username]
    return user_db


def fake_decode_token(token: str):
    user = get_user(fake_user_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Wrong credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if current_user["active"]:
        return current_user
    else:
        raise HTTPException(status_code=404, detail="휴면유저입니다.")


# Get user data
@router.get("/login_data")
async def read_me(user: dict = Depends(get_current_active_user)):
    return user


if __name__ == "__main__":
    uvicorn.run("oauth:app", reload=True)
