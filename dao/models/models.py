from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from typing import Optional


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True) 
    email: Mapped[Optional[str]]
    login: Mapped[str]
    name: Mapped[Optional[str]]
    lname: Mapped[Optional[str]]
    sex: Mapped[Optional[str]]
    """
    images: Mapped[list["Image"]] = relationship(
        "Image",
        back_populates="user",
        cascade="all, delete"
    )
    """

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, login={self.login}, name={self.name}, lname={self.lname}, sex={self.sex})"


class Audio(Base):
    __tablename__ = "audio"

    url_link_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(200))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    """
    user: Mapped[User] = relationship(
        "User",
        back_populates="images"
    )
    """

    def __repr__(self) -> str:
        return f"Image(url_link_id={self.url_link_id}, filename={self.filename}, user_id={self.user_id})"


class SuperUsers(Base):
    __tablename__ = "superusers"

    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"), primary_key=True)

