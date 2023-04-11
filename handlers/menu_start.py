from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from bot_config import ID, async_session
from database import db
from database.db import Users
from inline import entry_ikb
from keyboard import keyboard_menu
from message.contacts_message import MESSAGES_CONTACTS
from .service import FSMClient


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """
    Вывод стартового меню.
    Разделение на меню админа и пользователя.
    Сохранение данных пользователя для дальнейшего подсчета денег и отправки общего сообщения от админа.
    :param message: types.Message
    :return: message.answer
    """
    if message.from_user.id in ID:
        await db.sql_add_user(
            async_session,
            user=Users(
                id=message.from_user.id,
                full_name=message.from_user.full_name,
                admin=True,
            ),
        )
        await message.answer(
            f"Hello admin {message.from_user.username}\nМеню",
            reply_markup=keyboard_menu.main_menu_admin,
        )
    else:
        await db.sql_add_user(
            async_session,
            user=Users(
                id=message.from_user.id,
                full_name=message.from_user.full_name,
                admin=False,
            ),
        )
        await message.answer("Вас приветствует бот салона красоты ...")
        await message.answer("Меню", reply_markup=keyboard_menu.main_menu_user)

        await message.delete()


# @dp.message_handler(Text(equals=['Записаться'], ignore_case=True))
async def head_menu_handler(message: types.Message):
    """
    Отлавливание KeyboardButton 'Записаться' из чата с ботом,
    вывод InlineKeyboardMarkup и запуск машины состояния
    :param message: types.Message
    :return: message.answer
    """
    await message.delete()
    await message.answer(
        "Выберите услугу для записи: ", reply_markup=entry_ikb.buttons_entry_menu
    )
    await FSMClient.state_process.set()


# @dp.message_handler(Text(equals=['Контакты'], ignore_case=True))
async def price_from_main_menu(message: types.Message):
    """
    Отлавливание KeyboardButton 'Контакты' из чата с ботом,
    отправка сообщения админу или пользователю
    :param message: types.Message
    :return: message.answer
    """
    if message.from_user.id in ID:
        await message.answer(
            MESSAGES_CONTACTS["contacts"], reply_markup=keyboard_menu.main_menu_admin
        )
    else:
        await message.answer(
            MESSAGES_CONTACTS["contacts"], reply_markup=keyboard_menu.main_menu_user
        )


# @dp.message_handler(Text(equals=['Админ_панель'], ignore_case=True))
async def admin_menu_handler(message: types.Message):
    """
    Отлавливание KeyboardButton 'Админ_панель' из чата с ботом,
    вывод KeyboardButtons для админа
    :param message: types.Message
    :return: message.answer
    """
    if message.from_user.id in ID:
        await message.answer(text="Админ панель", reply_markup=keyboard_menu.admin_menu)


# Регистрация для выноса в MAIN
def registration_handler_start_menu(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=["start", "help", "Меню"])
    dp.register_message_handler(
        head_menu_handler, Text(equals=["Записаться"], ignore_case=True)
    )
    dp.register_message_handler(
        price_from_main_menu, Text(equals=["Контакты"], ignore_case=True)
    )
    dp.register_message_handler(
        admin_menu_handler, Text(equals=["Админ_панель"], ignore_case=True)
    )
