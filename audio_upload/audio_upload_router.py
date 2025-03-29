from typing import Annotated
from fastapi import APIRouter, File

router = APIRouter()


@router.post("/audio/", tags=["audio"])
async def read_users(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}
