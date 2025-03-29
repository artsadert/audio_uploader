from typing import Annotated
from fastapi import APIRouter, File

from dao import database

router = APIRouter()


@router.post("/audio/", tags=["audio"])
async def read_users(file: Annotated[bytes | None, File()] = None, token: str | None = None):
    if not file:
        return {"message": "No file sent"}
    elif not token:
        return {"message": "No token sent"}

    
