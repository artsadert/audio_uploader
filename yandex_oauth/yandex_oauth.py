from yandexid import AsyncYandexID, AsyncYandexOAuth


async def get_user_info(oauth: str):
    yandex_id = AsyncYandexID(oauth)

    return await yandex_id.get_user_info_json()

