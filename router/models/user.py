from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    """
    User model

    - id: identificator for user
    - email: email of user
    - login: login for user
    - name: name of user
    - lanme: lname of user
    - sex: sex of user
    """
    id: int
    login: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    lname: Optional[str] = None
    sex: Optional[str] = None
    

