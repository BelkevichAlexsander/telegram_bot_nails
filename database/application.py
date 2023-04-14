from sqlalchemy import ForeignKey, Result, ChunkedIteratorResult, select
from sqlalchemy.orm import Mapped, mapped_column

from database.Base import Base, AsyncSessionLocal


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


async def sql_add_application(date: Applications) -> None:
    """
    Добавление заявки в бд
    :param date: Applications
    :return: None
    """
    async with AsyncSessionLocal() as session:
        async with session.begin():
            session.add(date)


async def applications_date() -> Result[ChunkedIteratorResult]:
    """
    Получение одного элемента по индефикатору из таблицы users
    :return: ChunkedIteratorResult
    """
    async with AsyncSessionLocal() as session:
        request = select(Applications)

        return await session.execute(request)


async def select_date_application(date: str) -> Result[ChunkedIteratorResult]:
    """
    Получение списка занятых дат
    :param date: String
    :return: ChunkedIteratorResult
    """
    async with AsyncSessionLocal() as session:
        request = select(Applications).where(Applications.date == date)

        return await session.execute(request)
