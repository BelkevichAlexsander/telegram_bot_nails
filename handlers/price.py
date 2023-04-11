from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from bot_config import ID
from keyboard import keyboard_price, keyboard_menu
from message.price_message import MESSAGES_PRICE


# @dp.message_handler(Text(equals=['Цены'], ignore_case=True))
async def price_from_main_menu(message: Message):
    """
    Отлавливание KeyboardButton 'Цены' из чата с ботом,
    вывод KeyboardButtons по услугам
    :param message: types.Message
    :return: message.answer
    """
    await message.answer(
        MESSAGES_PRICE["service"], reply_markup=keyboard_price.menu_key_price
    )


# @dp.message_handler(commands=['Педикюр', 'Маникюр', 'Наращивание'])
async def menu_in_price(message: Message):
    """
    Отлавливание commands=['Педикюр', 'Маникюр', 'Наращивание'] из чата с ботом,
    вывод сообщений с ценами, а также кнопка возврата в меню
    :param message: types.Message
    :return: message.answer
    """
    if message.text == "Педикюр":
        await message.answer(
            MESSAGES_PRICE["pedicure"], reply_markup=keyboard_price.menu_key_price
        )
        await message.answer("Для записи к мастеру вернитесь в основное меню")

    if message.text == "Маникюр":
        await message.answer(
            MESSAGES_PRICE["manicure"], reply_markup=keyboard_price.menu_key_price
        )
        await message.answer("Для записи к мастеру вернитесь в основное меню")

    if message.text == "Наращивание":
        await message.answer(
            MESSAGES_PRICE["nail_extension"], reply_markup=keyboard_price.menu_key_price
        )
        await message.answer("Для записи к мастеру вернитесь в основное меню")

    if message.text == "Возврат в меню":
        if message.from_user.id in ID:
            await message.answer("Меню", reply_markup=keyboard_menu.main_menu_admin)
        else:
            await message.answer("Меню", reply_markup=keyboard_menu.main_menu_user)


def registration_handler_price(dp: Dispatcher):
    dp.register_message_handler(
        price_from_main_menu, Text(equals=["Цены"], ignore_case=True)
    )
    dp.register_message_handler(
        menu_in_price,
        Text(
            equals=["Педикюр", "Маникюр", "Наращивание", "Возврат в меню"],
            ignore_case=True,
        ),
    )
