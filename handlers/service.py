import copy

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, ID
from calendar_async import simple_cal_callback, SimpleCalendar
from database import application
from inline import time_ikb
from keyboard import keyboard_menu


class FSMClient(StatesGroup):
    """
    Машина состояний для формирования заказа
    """

    state_process = State()
    state_date = State()
    state_time = State()
    state_phone = State()


# @dp.callback_query_handler(state=FSMClient.state_process)
async def set_service(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Отлавливает старт машины состояния, заносит название услугу в память машины состояния,
    после останавливает машину состояния и запускает календарь для получения даты
    :param callback_query: types.CallbackQuery
    :param state: FSMContext
    :return: callback_query.message.answer
    """
    await callback_query.message.delete_reply_markup()
    await callback_query.message.delete()

    # Запись данных в "state".
    async with state.proxy() as data:
        data["state_process"] = callback_query.data

    # Здесь выполняется сброс "state". Календарь начинает работать.
    await state.reset_state(with_data=False)

    await callback_query.message.answer(
        "Выберите дату:", reply_markup=await SimpleCalendar().start_calendar()
    )


# @dp.callback_query_handler(simple_cal_callback.filter())
async def process_dialog_calendar(
    callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext
):
    """
    Отлавливает дату выбранную пользователем из календаря,
    стартует машину состояния для продолжения сохранения данных,
    заносит дату в память машины состоянияы
    :param callback_data: Dictionary
    :param callback_query: types.CallbackQuery
    :param state: FSMContext
    :return: callback_query.message.answer
    """
    selected, date = await SimpleCalendar().process_selection(
        callback_query, callback_data
    )
    if selected:
        # Снова запускаю "state"
        await FSMClient.state_date.set()

        # Запись даты в "state"
        async with state.proxy() as data:
            data["state_date"] = date.strftime("%d.%m.%Y")

        # Получение данных о записях в определенную дату
        time_applications = await application.select_date_application(
            date.strftime("%d.%m.%Y")
        )
        only_time: list = [x.time for x in time_applications.scalars()]

        # Глубокая копия для оптимизации удаления связей Dictionary с памятью
        time_check_btn: dict = copy.deepcopy(time_ikb.buttons_time_check)
        time_btn: types.InlineKeyboardMarkup = copy.deepcopy(time_ikb.buttons_time)

        if len(only_time) >= 4:
            await callback_query.message.answer(
                text=f'Свободного времени {date.strftime("%d.%m.%Y")} нет \n'
                f"Пожалуйста запишитесь на другой день.",
                reply_markup=keyboard_menu.main_menu_user,
            )
            await state.finish()

        else:
            for x in only_time:
                del time_check_btn[x]

            await callback_query.message.answer(
                text="Выберите свободное время:",
                reply_markup=time_btn.add(
                    *[btn for key, btn in time_check_btn.items()]
                ),
            )

            await callback_query.message.delete()
            await FSMClient.next()


# @dp.callback_query_handler(state=FSMClient.state_time)
async def set_time(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Отлавливает время выбранное пользователем, заносит время в память машины состояния
    :param callback_query: types.CallbackQuery
    :param state: FSMContext
    :return: callback_query.message.answer
    """
    # Запись данных в "state".
    async with state.proxy() as data:
        data["state_time"] = callback_query.data

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)
    )

    await callback_query.message.answer(
        text="Поделитесь номером телефона", reply_markup=keyboard
    )

    await FSMClient.next()


# @dp.message_handler(content_types=types.ContentType.CONTACT, state=FSMClient.state_phone)
async def contacts(message: types.Message, state: FSMContext):
    """
    Отлавливает телефон отправленный при записи, заносит номер телефона в память машины состояния,
    после останавливает машину состояния и сохраняет данные в бд и отправлеят результаты заказа
    пользователю и админу
    :param message: types.Message
    :param state: FSMContext
    :return: bot.send_message
    """
    await message.delete()
    # Запись данных в "state".
    async with state.proxy() as data:
        if message.text:
            data["state_phone"] = message.text
        else:
            data["state_phone"] = message.contact.phone_number
    await state.finish()

    # date : tuple(full_name: str, service: str, date: str, time: str, state_phone: str, id_user: str)
    await application.sql_add_application(
        date=application.Applications(
            full_name=message.chat.full_name,
            service=data["state_process"],
            date=data["state_date"],
            time=data["state_time"],
            number=data["state_phone"],
            id_user=message.chat.id,
        ),
    )

    await bot.send_message(
        message.chat.id,
        text=f"Запись осуществлена!\n "
        f"Имя: {message.chat.full_name}\n"
        f'Услуга: {data["state_process"]}\n'
        f'Дата: {data["state_date"]}\n'
        f'Время: {data["state_time"]}\n'
        f'Телефон: {data["state_phone"]}\n',
        reply_markup=keyboard_menu.main_menu_admin,
    )

    await bot.send_message(
        chat_id=ID[0],
        text=f"Клиент:\n "
        f"id: {message.chat.id}\n "
        f"Имя: {message.chat.full_name}\n"
        f'Услуга: {data["state_process"]}\n'
        f'Дата: {data["state_date"]}\n'
        f'Время: {data["state_time"]}\n'
        f'Телефон: {data["state_phone"]}\n'
        f"User_name: @{message.chat.username}",
    )


def register_handlers_client_service(dp: Dispatcher):
    dp.register_callback_query_handler(set_service, state=FSMClient.state_process)
    dp.register_callback_query_handler(
        process_dialog_calendar, simple_cal_callback.filter()
    )
    dp.register_callback_query_handler(set_time, state=FSMClient.state_time)
    dp.register_message_handler(
        contacts,
        content_types=[types.ContentType.CONTACT, types.ContentType.TEXT],
        state=FSMClient.state_phone,
    )
