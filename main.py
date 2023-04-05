import logging

from aiogram.utils import executor

from bot_config import dp
from database import sqlite_db
from handlers import admin, menu_start, price, service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()

    menu_start.registration_handler_start_menu(dp=dp)
    service.register_handlers_client_service(dp=dp)
    price.registration_handler_price(dp=dp)
    admin.registration_handler_admin(dp=dp)

if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
