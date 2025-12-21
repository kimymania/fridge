from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from service import user as service

router = APIRouter(prefix="/login")

templates = Jinja2Templates(directory="templates")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def unauth():
    raise HTTPException(
        status_code=404,
        detail="Wrong credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
    )


@router.post("/", response_class=HTMLResponse)
def login(
    request: Request,
    response: Response,
    user_name: Annotated[str, Form(...)],
    user_password: Annotated[str, Form(...)],
):
    user = service.auth_user(user_name, user_password)
    if not user:
        unauth()
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.name},
        expire=expire,
    )
    response = RedirectResponse("/html", status_code=302)
    response.set_cookie(key="token", value=access_token)
    return response
