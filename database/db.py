from __future__ import annotations

from typing import Any

from sqlalchemy import ForeignKey, select, Result, ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    admin: Mapped[bool]

    def __str__(self):
        return f"{self.id}: {self.full_name} \n"


class Applications(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    service: Mapped[str]
    date: Mapped[str]
    time: Mapped[str]
    number: Mapped[str]
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __str__(self):
        return (
            f"Заказчик: {self.full_name}\n"
            f"Услуга: {self.service}\n"
            f"Дата и время: {self.date} {self.time}\n"
            f"Телефон: {self.number}\n"
        )


async def sql_add_user(
    async_session: async_sessionmaker[AsyncSession], user: Users
) -> None:
    """
    Добавление пользователя в бд, когда тот вызывает меню у бота
    :param async_session: AsyncSession
    :param user: Users
    :return: None
    """
    async with async_session() as session:
        async with session.begin():
            session.add(user)


async def sql_add_application(
    async_session: async_sessionmaker[AsyncSession], date: Applications
) -> None:
    """
    Добавление заявки в бд
    :param async_session: AsyncSession
    :param date: Applications
    :return: None
    """
    async with async_session() as session:
        async with session.begin():
            session.add(date)


async def all_users(
    async_session: async_sessionmaker[AsyncSession],
) -> Result[Any]:
    """
    Выборка всей таблицы users
    :param async_session: AsyncSession
    :return: None
    """
    async with async_session() as session:
        request = select(Users).where(Users.admin == 0)

        return await session.execute(request)


async def applications_date(
    async_session: async_sessionmaker[AsyncSession],
) -> Result[ChunkedIteratorResult]:
    """
    Получение одного элемента по индефикатору из таблицы users
    :param async_session: AsyncSession
    :return: ChunkedIteratorResult
    """
    async with async_session() as session:
        request = select(Applications)

        return await session.execute(request)


async def select_date_application(
    date: str,
    async_session: async_sessionmaker[AsyncSession],
) -> Result[ChunkedIteratorResult]:
    """
    Получение списка занятых дат
    :param date: String
    :param async_session: AsyncSession
    :return: ChunkedIteratorResult
    """
    async with async_session() as session:
        request = select(Applications).where(Applications.date == date)

        return await session.execute(request)


async def create_db(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
