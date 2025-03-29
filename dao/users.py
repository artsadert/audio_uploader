from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from os import getenv

import loading_dotenv
from models import models



loading_dotenv.load()


def create_user():
    pass

def delete_user():
    pass

def create_image():
    pass






engine = create_engine(str(getenv("PGLINK")))
models.Base.metadata.create_all(engine)

with Session(engine) as session:
    stmt = select(models.User)
    for user in session.scalars(stmt):
        print(user)
