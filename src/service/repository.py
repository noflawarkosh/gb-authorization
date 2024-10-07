from sqlalchemy import update, and_, func, text, select

from service.models import UserSessionModel, UserModel
from database import async_session_factory
from service.schemas import UserCreateSchema, UserLoginSchema, UserSessionCreateSchema
from service.utils import Password


class Repository:

    @classmethod
    async def register(cls, data: UserCreateSchema) -> UserModel:
        try:
            async with async_session_factory() as session:

                query = text('SELECT user_default_access_level from crm_settings where id = 1')
                db_response = await session.execute(query)
                default_access_level = db_response.first()[0] if db_response else None

                if not default_access_level:
                    raise Exception('0x000001')

                data.email = data.email.lower()
                data.username = data.username.lower()
                data.password = Password.hmac(data.password)

                user = UserModel(
                    **{
                        **data.dict(),
                        'access_level': default_access_level
                    }
                )

                session.add(user)
                await session.commit()
                await session.refresh(user)

                return user

        finally:
            await session.close()

    @classmethod
    async def get_user_by_username(cls, username: str) -> UserModel:

        try:
            async with async_session_factory() as session:

                query = (
                    select(UserModel)
                    .where(UserModel.username == username.lower())
                )
                db_response = await session.execute(query)
                user = db_response.scalars().one_or_none()
                return user if user else None

        finally:
            await session.close()

    @classmethod
    async def login(cls, data: UserSessionCreateSchema) -> UserSessionModel:

        try:
            async with async_session_factory() as session:
                user_session = UserSessionModel(**data.dict())
                session.add(user_session)
                await session.commit()
                await session.refresh(user_session)
                return user_session
        finally:
            await session.close()

    @classmethod
    async def expire_sessions(cls, user_id: int, exclude_token: str = None):
        try:
            async with async_session_factory() as session:

                query = update(UserSessionModel)

                if exclude_token:
                    query = query.where(
                        and_(
                            UserSessionModel.token != exclude_token,
                            UserSessionModel.user_id == user_id
                        )
                    )
                else:
                    query = query.where(UserSessionModel.user_id == user_id)

                query = query.values(expires=func.now())

                await session.execute(query)
                await session.commit()

        finally:
            await session.close()
