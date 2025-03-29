from yandexid import AsyncYandexID, AsyncYandexOAuth

from os import getenv


async def get_user_info(oauth_token: str):
    yandex_id = AsyncYandexID(oauth_token)

    return await yandex_id.get_user_info_json()


async def reload_token_using_refresh(refresh_token: str):
    yandex_id = AsyncYandexOAuth(
        client_id=str(getenv("client_id")),
        client_secret=str(getenv("client_secret")),
        redirect_uri=str(getenv("localhost:8000/docs"))
    )
    return await yandex_id.get_token_from_refresh_token(refresh_token=refresh_token)

