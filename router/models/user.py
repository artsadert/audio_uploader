from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    email: Optional[str]
    login: str
    name: Optional[str]
    lname: Optional[str]
    sex: Optional[str]
    

