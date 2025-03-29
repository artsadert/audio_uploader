from fastapi import APIRouter, HTTPException, status

from dao import database
from router.models.user import User
from yandex_oauth import yandex_oauth

router = APIRouter()

@router.delete("/user")
async def delete_user(userid: int, oauth_token: str):
    result = await yandex_oauth.get_user_info(oauth_token)
    if not database.is_super_user(int(result.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access denied',
        )
    
    database.delete_user(userid)
    return {"message": "user is deleted"}

@router.get("/user")
async def get_user_info(id_to_get: int, oauth_token: str):
    if not database.check_is_user_existing(id_to_get):
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

    
    return database.get_user_info(id_to_get)

@router.put("/user")
async def update_user_info(user: User, oauth_token: str):
    if not database.check_is_user_existing(user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found',
        )

    result = await yandex_oauth.get_user_info(oauth_token)
    if user.id != int(result.id) and not database.is_super_user(int(result.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access denied',
        )
    
    database.update_user_info(user.id, user.email, user.login, user.name, user.lname, user.sex)


