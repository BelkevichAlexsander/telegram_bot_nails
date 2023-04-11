import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import config

loop = asyncio.get_event_loop()
storage = MemoryStorage()

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(
    bot=bot, storage=storage, loop=loop
)  # (bot=bot, storage=storage) if MemoryStorage

# ADMIN ID
ID = [
    int(config.id_admin.get_secret_value()),
    # int(config.config.id_admin_telegram_2.get_secret_value())
]

# DB
engine_db = create_async_engine(
    # "postgresql+asyncpg://scott:tiger@localhost/test",
    config.db_connect.get_secret_value(),
    echo=True,
)

# async_sessionmaker: a factory for new AsyncSession objects.
# expire_on_commit - don't expire objects after transaction commit
async_session = async_sessionmaker(engine_db, expire_on_commit=False)
