from fastapi import APIRouter, Cookie, HTTPException, Header, Response, status
from yandex_oauth import yandex_oauth

from dao import database

from typing import Annotated


router = APIRouter()


@router.post("/auth",
            summary="Log up user")
async def create_user(oauth_token: Annotated[str, Header()]):
    """
    Log up user using oauth_token

    - **oauth_token**(Header): required token given by https://oauth.yandex.ru
    """
    result = await yandex_oauth.get_user_info(oauth_token)
    await database.create_user(int(result.id), result.default_email, result.login, result.first_name, result.last_name, result.sex)

    return {"created user": result.login}


@router.post("/login",
            summary="Log in user")
async def login_user(oauth_token: Annotated[str, Header()]):
    """
    Log in user using oauth_token

    - **oauth_token**(Header): required token given by https://oauth.yandex.ru
    """
    return await yandex_oauth.get_user_info(oauth_token)

@router.post("/reload",
             summary="Reaload tokens")
async def reload_tokens(refresh_token: Annotated[str | None, Cookie()], response: Response):
    """
    Reaload tokens usinng refresh token
    - **refresh_token**(Cookie): required token to refresh both access and refresh token
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No refresh token provided"
        )

    result = await yandex_oauth.reload_token_using_refresh(str(refresh_token))
    response.set_cookie(key="refresh_token", value=result.refresh_token, httponly=True)

    return {"tokens": result}

