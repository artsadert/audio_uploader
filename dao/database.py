from fastapi import UploadFile
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from os import getenv, mkdir, path, remove

from dao import loading_dotenv
from dao.models import models



loading_dotenv.load()

engine = create_engine(str(getenv("PGLINK")))


async def create_user(id: int, email: str | None, login: str, name: str | None, lname: str | None, sex: str | None) -> int:
    user_id = None
    with Session(engine) as session:
        user = models.User(id=id, email=email, login=login, name=name, lname=lname, sex=sex)
        session.add(user)

        session.commit()
        user_id = user.id

    if not user_id:
        raise ValueError

    return user_id


async def delete_user(id: int):
    tracks = await get_list_audio(id)
    for track in tracks:
        try:
            remove(f"audios/{track['filepath']}")
        except:
            print(f"no such file: {track['filepath']}")
    with Session(engine) as session:
        session.query(models.User).filter(models.User.id == id).delete()
        session.commit()




async def get_user_info(id: int) -> models.User:
    user = None
    with Session(engine) as session:
        user = session.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise ValueError

    return user

async def update_user_info(id: int | None, email: str | None, login: str, name: str | None, lname: str | None, sex: str | None) -> models.User:
    user = None
    with Session(engine) as session:
        stmt = select(models.User).where(models.User.id == id)
        user = session.scalars(stmt).one()

        user.email = email
        user.login = login
        user.name = name
        user.lname = lname
        user.sex = sex

        session.commit()

    return user


async def check_is_user_existing(id: int) -> bool:
    user = None
    with Session(engine) as session:
        stmt = select(models.User).where(models.User.id == id)
        user = session.scalars(stmt).one_or_none()

    return user is not None



async def create_audio(filename: str, file: UploadFile, id: int) -> int:
    image_id = None
    with Session(engine) as session:
        image = models.Audio(filename=filename, user_id=id) 
        session.add(image)

        session.commit()
        image_id = image.url_link_id

    if not image_id:
        raise ValueError


    if not path.isdir("./audios"):
        mkdir("./audios")
    with open(f"./audios/{image_id}", 'wb') as f:
        content = await file.read()
        f.write(content)

    return image_id

async def get_list_audio(id: int) -> list[dict[str, str]]:
    tracks = []
    with Session(engine) as session:
        stmt = select(models.Audio).where(models.Audio.user_id == id)
        for track in session.scalars(stmt):
            tracks.append({"filename": track.filename, "filepath": track.url_link_id})

    return tracks


async def is_super_user(id: int) -> bool:
    superuser = None
    with Session(engine) as session:
        stmt = select(models.SuperUsers).where(models.SuperUsers.user_id == id)
        superuser = session.scalars(stmt).one_or_none()

    return superuser is not None


def update_table():
    #models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)



