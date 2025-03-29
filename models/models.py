from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from typing import Optional


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True) 
    email: Mapped[str]
    login: Mapped[str]
    name: Mapped[str]
    lname: Mapped[str]
    sex: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, login={self.login}, name={self.name}, lname={self.lname}, sex={self.sex})"


class Image(Base):
    __tablename__ = "image"

    url_link_id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"Image(url_link_id={self.url_link_id}, filename={self.filename}, user_id={self.user_id})"
