from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# button menu entry
button_pedicure = InlineKeyboardButton(text='Педикюр', callback_data='Педикюр')
button_manicure = InlineKeyboardButton(text='Маникюр', callback_data='Маникюр')
button_nail_extension = InlineKeyboardButton(text='Наращивание', callback_data='Наращивание')
button_complex = InlineKeyboardButton(text='Комплекс (Педикюр и Маникюр)', callback_data='Комплекс')

buttons_entry_menu = InlineKeyboardMarkup(row_width=1)
buttons_entry_menu.add(button_pedicure, button_manicure, button_nail_extension, button_complex)
