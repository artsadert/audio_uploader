from typing import Annotated
from fastapi import APIRouter, File, HTTPException, status
import mimetypes

from dao import database
from yandex_oauth import yandex_oauth


router = APIRouter()


@router.post("/audio")
async def upload_track(file: Annotated[bytes | None, File()], filename: str, oauth_token: str):
    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None or not mime_type.startswith('audio'):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f'File {filename} has unsupported extension type',
        )

    # Todo verify that user 
    result = await yandex_oauth.get_user_info(oauth_token)
    if not database.check_is_user_existing(result.psuid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'File {filename} has unsupported extension type',
        )

    database.create_audio(filename, file, result.psuid)





    
@router.get("/audio/user")
async def get_all_user_audio(psuid: str, oauth_token: str):
    if not database.check_is_user_existing(psuid):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found',
        )

    result = await yandex_oauth.get_user_info(oauth_token)
    if psuid != result.psuid and not database.is_super_user(result.psuid):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access denied',
        )
    
    
    return {"tracks": database.get_list_audio(psuid)}
