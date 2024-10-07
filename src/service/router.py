import datetime
from io import BytesIO
from typing import Annotated, List, Optional
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Depends, Response, Request, HTTPException, File, UploadFile
from sqlalchemy import func

import config
from service.repository import Repository
from service.strings import *

from service.schemas import UserReadSchema, UserCreateSchema, UserUpdateSchema, UserLoginSchema, \
    UserSessionCreateSchema, UserSessionReadSchema
from service.utils import StringGenerator, Password

router = APIRouter(tags=["Authorization"])


@router.post('/register')
async def register(data: Annotated[UserCreateSchema, Depends()]):
    try:
        user = await Repository.register(data)
        return UserReadSchema.model_validate(user, from_attributes=True)

    except IntegrityError as e:
        if e.orig.pgcode == '23505':
            raise HTTPException(status_code=409, detail=str(e.orig).split('DETAIL:  ')[1])
        else:
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/login')
async def login(request: Request, response: Response, data: Annotated[UserLoginSchema, Depends()]):
    user = await Repository.get_user_by_username(data.username)

    if not user:
        raise HTTPException(status_code=404, detail='0x000003')

    if Password.hmac(data.password) != user.password:
        raise HTTPException(status_code=403, detail='0x000003')

    if not 1 & user.access_level:
        raise HTTPException(status_code=403, detail='0x000004')

    token = StringGenerator.alphanumeric(128)
    session = UserSessionCreateSchema.model_validate(
        {
            'user_id': user.id,
            'token': token,
            'useragent': request.headers.get('user-agent'),
            'ip': request.client.host,
            'dt_expires': datetime.datetime.now() + datetime.timedelta(days=3),
        }
    )

    session = await Repository.login(session)
    response.set_cookie(key=config.COOKIE_KEY, value=token)
    return UserSessionReadSchema.model_validate(session, from_attributes=True)
