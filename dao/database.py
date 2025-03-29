from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from os import getenv

import loading_dotenv
from models import models



loading_dotenv.load()

engine = create_engine(str(getenv("PGLINK")))


def create_user():
    with Session(engine) as session:


        session.commit()

def delete_user():
    pass

def create_image(filename: str, file: bytes, user_id: int):
    image_id = None
    with Session(engine) as session:
        image = models.Image(filename=filename, user_id=user_id) 
        session.add(image)

        session.commit()
        image_id = image.url_link_id

    if not image_id:
        raise ValueError


    with open(f"./files/{image_id}", 'wb') as f:
        f.write(file)



def get_all():
    with Session(engine) as session:
        stmt = select(models.User)
        for user in session.scalars(stmt):
            print(user)
        stmt = select(models.Image)
        for user in session.scalars(stmt):
            print(user)




if __name__ == "__main__":
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)
    with Session(engine) as session:
        user = models.User(email="artsadert@gmail.com", login="art", name="arthur", lname="sad", sex="m")
        session.add(user)
        session.commit()

    create_image("favsong.mp4", b'345345', 1)
    get_all()

