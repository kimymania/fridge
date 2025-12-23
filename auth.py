from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from model.user import User

SECRET_KEY = "9A2D253F008E9667ECE093F3C427CC8689107B3299172E3C5DE0DF65AA24125E"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user: User):
    data: dict[str, Any] = {"sub": user.name}
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.now()
    data.update({"exp": now + expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
