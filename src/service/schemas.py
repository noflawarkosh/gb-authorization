from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class UserSessionCreateSchema(BaseModel):
    user_id: int
    token: str
    useragent: str
    ip: str
    dt_expires: datetime


class UserSessionReadSchema(UserSessionCreateSchema):
    id: int
    dt_created: datetime


class UserLoginSchema(BaseModel):
    username: constr(min_length=5, max_length=20)
    password: constr(min_length=8, max_length=20)



class UserCreateSchema(BaseModel):
    name: constr(max_length=50)
    username: constr(min_length=5, max_length=20)
    email: constr(max_length=100)
    telnum: constr(min_length=11, max_length=11)
    telegram: constr(max_length=50)
    password: constr(min_length=8, max_length=16)


class UserUpdateSchema(BaseModel):
    name: constr(max_length=50)
    email: constr(max_length=100)
    telnum: constr(min_length=12, max_length=12)
    telegram: constr(max_length=50)


class UserReadSchema(BaseModel):
    id: int
    name: str
    username: str
    email: str
    telnum: str
    telegram: str
    dt_created: datetime
    access_level: int
    media: Optional[str] = None
