import boto3
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import (DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, S3KID, S3KEY, S3BUCKET)


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(url=f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
async_session_factory = async_sessionmaker(async_engine)

s3 = boto3.session.Session().client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=S3KID,
    aws_secret_access_key=S3KEY
)
