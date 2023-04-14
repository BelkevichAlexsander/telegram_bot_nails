import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """
    Для подгрузки секретных ключей и иных значений
    """

    bot_token: SecretStr
    id_admin: SecretStr
    db_connect: SecretStr

    class Config:
        """
        Вложенный класс с дополнительными указаниями для настроек.
        Получение данных из .env в переменные выше
        """

        dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)


# Валидация объекта конфига
config = Settings()

# ADMIN ID
ID = [
    int(config.id_admin.get_secret_value()),
    # int(config.config.id_admin_telegram_2.get_secret_value())
]

loop = asyncio.get_event_loop()
storage = MemoryStorage()

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(bot=bot, storage=storage, loop=loop)
