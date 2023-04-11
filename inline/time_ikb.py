from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# button menu entry
button_first = InlineKeyboardButton(text="09:00", callback_data="09:00")
button_second = InlineKeyboardButton(text="11:30", callback_data="11:30")
button_third = InlineKeyboardButton(text="14:00", callback_data="14:00")
button_forth = InlineKeyboardButton(text="16:30", callback_data="16:30")

# menu user
buttons_time = InlineKeyboardMarkup(row_width=1)


buttons_time_check = {
    "09:00": button_first,
    "11:30": button_second,
    "14:00": button_third,
    "16:30": button_forth,
}
