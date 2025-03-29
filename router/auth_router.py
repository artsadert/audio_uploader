from fastapi import APIRouter
from yandex_oauth import yandex_oauth

from dao import database

router = APIRouter()


@router.post("/auth")
async def create_user(oauth_token: str):
    result = await yandex_oauth.get_user_info(oauth_token)
    database.create_user(result.psuid, result.default_email, result.login, result.first_name, result.last_name, result.sex)

    return {"message": result}

