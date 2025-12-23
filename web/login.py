from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from auth import create_access_token, unauth
from error import Duplicate
from service import user as service

router = APIRouter(tags=["login"])

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.post("/login", response_class=HTMLResponse)
def login(
    response: Response,
    user_name: Annotated[str, Form(...)],
    user_password: Annotated[str, Form(...)],
):
    user = service.auth_user(user_name, user_password)
    if not user:
        raise unauth()
    else:
        access_token = create_access_token(user)
        response = RedirectResponse("/fridge", status_code=302)
        response.set_cookie(key="token", value=access_token)
        return response


@router.post("/login/signup", response_class=HTMLResponse)
def signup(
    user_name: Annotated[str, Form(...)],
    user_password: Annotated[str, Form(...)],
    password_check: Annotated[str, Form(...)],
):
    if user_password != password_check:
        raise HTTPException(status_code=401, detail="비밀번호와 비밀번호 확인이 일치하지 않습니다")
    try:
        service.create_user(user_name, user_password)
    except Duplicate:
        raise HTTPException(status_code=409, detail="이미 등록된 아이디입니다")
    return RedirectResponse("/login", status_code=302)


@router.post("/logout", response_class=HTMLResponse)
def logout():
    return RedirectResponse("/login", status_code=302)
