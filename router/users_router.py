from typing import Annotated

from fastapi import APIRouter, HTTPException, Header, status

from dao import database
from router.models.user import User
from yandex_oauth import yandex_oauth


router = APIRouter(prefix="/user")


@router.delete("/",
               summary="Deletes user account")
async def delete_user(userid: int, oauth_token: Annotated[str, Header()]):
    """
    Deletes user account
    Only superuser can deleted user account or it's owner

    - **userid**: user to delete
    - **oauth_token**(Header): required token given by https://oauth.yandex.ru
    """
    result = await yandex_oauth.get_user_info(oauth_token)
    if not await database.is_super_user(int(result.id)) and userid != int(result.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access denied',
        )
    
    await database.delete_user(userid)
    return {"message": "user is deleted", "id": userid}

@router.get("/",
            summary="Gets information about user",
            response_model=User)
async def get_user_info(id_to_get: int, oauth_token: Annotated[str, Header()]):
    """
    Get information about user
    Only superuser can see user account or it's owner if it's private

    - **id_to_get**: user to delete
    - **oauth_token**(Header): required token given by https://oauth.yandex.ru
    """
    if not await database.check_is_user_existing(id_to_get):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found',
        )
    user = await yandex_oauth.get_user_info(oauth_token)

    if user.id != id_to_get:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access denied',
        )

    
    return await database.get_user_info(id_to_get)

@router.patch("/",
            summary="Change information about user",
            include_in_schema=True)
async def update_user_info(user: User, oauth_token: Annotated[str, Header()]):
    """
    update information about user

    - **id**: identificator for user
    - **email**: email of user
    - **login**: login for user
    - **name**: name of user
    - **lanme**: lname of user
    - **sex**: sex of user

    - **oauth_token**(Header): required token given by https://oauth.yandex.ru
    """
    if not await database.check_is_user_existing(user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found',
        )

    result = await yandex_oauth.get_user_info(oauth_token)
    if user.id != int(result.id) and not await database.is_super_user(int(result.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access denied',
        )
    
    print("resoponding")
    await database.update_user_info(user.id, user.login, user.email, user.name, user.lname, user.sex)
    return await database.get_user_info(user.id)


