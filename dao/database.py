from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from os import getenv, mkdir, path

from dao import loading_dotenv
from dao.models import models



loading_dotenv.load()

engine = create_engine(str(getenv("PGLINK")))


def create_user(id: int, email: str | None, login: str, name: str | None, lname: str | None, sex: str | None):
    user_id = None
    with Session(engine) as session:
        user = models.User(id=id, email=email, login=login, name=name, lname=lname, sex=sex)
        session.add(user)

        session.commit()
        user_id = user.id

    if not user_id:
        raise ValueError

    return user_id


def delete_user(id: int):
    with Session(engine) as session:
        session.query(models.User).filter(models.User.id == id).delete()
        session.commit()


def get_user_info(id: int):
    user = None
    with Session(engine) as session:
        user = session.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise ValueError

    return user

def update_user_info(id: int | None, email: str | None, login: str, name: str | None, lname: str | None, sex: str | None):
    with Session(engine) as session:
        stmt = select(models.User).where(models.User.id == id)
        user = session.scalars(stmt).one()

        user.email = email
        user.login = login
        user.name = name
        user.lname = lname
        user.sex = sex

        session.commit()


def check_is_user_existing(id: int):
    user = None
    with Session(engine) as session:
        stmt = select(models.User).where(models.User.id == id)
        user = session.scalars(stmt).one_or_none()

    return user is not None



def create_audio(filename: str, file: bytes, id: int):
    image_id = None
    with Session(engine) as session:
        image = models.Audio(filename=filename, user_id=id) 
        session.add(image)

        session.commit()
        image_id = image.url_link_id

    if not image_id:
        raise ValueError


    if not path.isdir("./files"):
        mkdir("./files")
    with open(f"./files/{image_id}", 'wb') as f:
        f.write(file)

def get_list_audio(id: int) -> list[dict[str, str]]:
    tracks = []
    with Session(engine) as session:
        stmt = select(models.Audio).where(models.Audio.user_id == id)
        for track in session.scalars(stmt):
            tracks.append({"filename": track.filename, "filepath": track.url_link_id})

    return tracks

def is_super_user(id: int):
    superuser = None
    with Session(engine) as session:
        stmt = select(models.SuperUsers).where(models.SuperUsers.user_id == id)
        superuser = session.scalars(stmt).one_or_none()

    return superuser is not None


def update_table():
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)




if __name__ == "__main__":
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)

    with Session(engine) as session:
        user = models.User(email="artsadert@gmail.com", login="art", name="arthur", lname="sad", sex="m")
        session.add(user)
        session.commit()

    create_image("favsong.mp4", b'345345', 1)
    get_all()

