from router import auth_router, audio_router, users_router
from fastapi import FastAPI
from dao import database

database.update_table()


app = FastAPI()


app.include_router(auth_router.router, tags=["auth"])
app.include_router(audio_router.router, tags=["audio"])
app.include_router(users_router.router, tags=["user"])
