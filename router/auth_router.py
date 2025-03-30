from fastapi import APIRouter, Cookie, HTTPException, Header, status
from yandex_oauth import yandex_oauth

from dao import database

from typing import Annotated

router = APIRouter()


@router.post("/auth")
async def create_user(oauth_token: Annotated[str, Header()]):
    result = await yandex_oauth.get_user_info(oauth_token)
    await database.create_user(int(result.id), result.default_email, result.login, result.first_name, result.last_name, result.sex)

    return {"message": result}

@router.post("/reload")
async def reload_tokens(refresh_token: Annotated[str | None, Cookie()]):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No refresh token provided"
        )
    return await yandex_oauth.reload_token_using_refresh(str(refresh_token))
