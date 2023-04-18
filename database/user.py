from typing import Any

from sqlalchemy import Result, select
from sqlalchemy.orm import Mapped, mapped_column

from database.base_model import Base
from .config_db import AsyncSessionLocal


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    admin: Mapped[bool]

    def __str__(self):
        return f"{self.id}: {self.full_name} \n"


async def sql_add_user(user: Users) -> None:
    """
    Добавление пользователя в бд, когда тот вызывает меню у бота
    :param user: Users
    :return: None
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(user)


async def all_users() -> Result[Any]:
    """
    Выборка всей таблицы users
    :return: None
    """
    async with AsyncSessionLocal() as session:
        request = select(Users)

        return await session.execute(request)
