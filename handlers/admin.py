from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked

from config import bot, ID
from database import user, application
from keyboard import keyboard_menu


# @dp.message_handler(Text(equals=['Пользователи'], ignore_case=True))
async def select_all_user_handler(message: types.Message):
    """
    Отлавливание KeyboardButton 'Пользователи' из чата с ботом
    и отправка сообщения админу о всех пользователей бота
    :param message: types.Message
    :return: message.answer
    """
    if message.from_user.id in ID:
        users = await user.all_users()

        await message.answer(
            text=f"{chr(10).join(str(x) for x in users.scalars())}",
            reply_markup=keyboard_menu.admin_menu,
        )


# @dp.message_handler(Text(equals=['Заказы'], ignore_case=True))
async def select_applications_handler(message: types.Message):
    """
    Отлавливание KeyboardButton 'Заказы' из чата с ботом
    и отправка сообщения админу о всех зарегистрированных заказах
    :param message: types.Message
    :return: message.answer
    """
    if message.from_user.id in ID:
        applications = await application.applications_date()
        await message.answer(
            f"{chr(10).join(str(x) for x in applications.scalars())}",
            reply_markup=keyboard_menu.admin_menu,
        )


# @dp.message_handler(Text(equals=['Отправить сообщение всем пользователям бота'], ignore_case=True))
async def message_all_user_handler(message: types.Message):
    """
    Отлавливание KeyboardButton 'Отправить сообщение всем пользователям бота'
    из чата с ботом и отправка сообщения админу
    :param message: types.Message
    :return: message.answer
    """
    if message.from_user.id in ID:
        await message.answer(text="Введи текст для всех пользователей Бота")


# @dp.message_handler()
async def spent_all_message(message: types.Message):
    """
    Функция только для админа.
    Делает выборку из бд всех пользователей и рассылает им отловленное сообщение от админа.
    :param message: types.Message
    :return: message.answer
    """
    if message.from_user.id in ID:
        users = await user.all_users()
        for user_s in users.scalars():
            try:
                await bot.send_message(
                    user_s.id,
                    text=f"Уважаемый(ая) {user_s.full_name}.\n {message.text}",
                )
            except BotBlocked:
                await message.answer(f"Blocked bot by {user_s.full_name}")
        await message.answer(f"Рассылка завершена! Всем пользователям!")
        await message.answer("Админ панель.", reply_markup=keyboard_menu.admin_menu)


# Регистрация для выноса в MAIN
def registration_handler_admin(dp: Dispatcher):
    dp.register_message_handler(
        select_all_user_handler, Text(equals=["Пользователи"], ignore_case=True)
    )
    dp.register_message_handler(
        select_applications_handler, Text(equals=["Заказы"], ignore_case=True)
    )
    dp.register_message_handler(
        message_all_user_handler,
        Text(equals=["Отправить сообщение всем пользователям бота"], ignore_case=True),
    )

    dp.register_message_handler(spent_all_message)
