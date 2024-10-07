import datetime
from typing import Annotated
from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

pk = Annotated[int, mapped_column(primary_key=True)]
dt = Annotated[datetime.datetime, mapped_column(server_default=text('NOW()'))]


class UserModel(Base):
    __tablename__ = 'authorization_user'

    id: Mapped[pk]
    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    telnum: Mapped[str] = mapped_column(unique=True)
    telegram: Mapped[str] = mapped_column(unique=True)
    dt_created: Mapped[dt]
    password: Mapped[str]
    access_level: Mapped[int]
    media: Mapped[str | None]


class UserSessionModel(Base):
    __tablename__ = 'authorization_user_session'

    id: Mapped[pk]
    token: Mapped[str]
    useragent: Mapped[str]
    ip: Mapped[str]
    dt_created: Mapped[dt]
    dt_expires: Mapped[datetime.datetime]

    # FK
    user_id: Mapped[int] = mapped_column(
        ForeignKey('authorization_user.id', ondelete='CASCADE', onupdate='CASCADE')
    )
