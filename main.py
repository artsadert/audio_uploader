from auth import auth_router
from audio_upload import audio_upload_router 
from fastapi import FastAPI


app = FastAPI()


app.include_router(auth_router.router)
app.include_router(audio_upload_router.router)
