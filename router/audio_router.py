from typing import Annotated
from fastapi import APIRouter, File, HTTPException, UploadFile, status, Header

from dao import database
from yandex_oauth import yandex_oauth


router = APIRouter()


@router.post("/audio",
             summary="Uploads audio file")
async def upload_track(file: UploadFile, filename: str | None, oauth_token: Annotated[str, Header()]):
    """
    Uploads audio file, filename can be changed

    - **file**: file to upload
    - **filename**: filename to use, not required
    - **oauth_token**(Header): required token given by https://oauth.yandex.ru
    """
    if not file.content_type.startswith("audio"):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f'File {filename} has unsupported extension type',
        )

    # Todo verify that user 
    result = await yandex_oauth.get_user_info(oauth_token)
    if not await database.check_is_user_existing(int(result.id)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'File {filename} has unsupported extension type',
        )

    await database.create_audio(str(filename) if filename else file.filename, file, int(result.id))

    return {"audio": {"filename": str(filename) if filename else file.filename, "filepath": f"audio/{result.id}"}}

    
@router.get("/audio/user",
            summary="get all user audio")
async def get_all_user_audio(id: int, oauth_token: Annotated[str, Header()]):
    """
    Get all user audio by id

    - **id**: id of user to get list of audiofiles's filename
    - **oauth_token**(Header): required token given by https://oauth.yandex.ru
    """
    if not await database.check_is_user_existing(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found',
        )

    result = await yandex_oauth.get_user_info(oauth_token)
    if id != int(result.id) and not await database.is_super_user(int(result.id)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access denied',
        )
    
    
    return {"tracks": await database.get_list_audio(id)}
