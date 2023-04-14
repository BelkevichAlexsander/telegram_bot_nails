from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import config


class Base(DeclarativeBase):
    pass


# DB
engine = create_async_engine(
    config.db_connect.get_secret_value(),
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False)
