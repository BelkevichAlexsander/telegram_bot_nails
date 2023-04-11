from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# меню вложеное в кнопку 'Цены'
ped = KeyboardButton("Педикюр")
man = KeyboardButton("Маникюр")
nar = KeyboardButton("Наращивание")
menu = KeyboardButton("Возврат в меню")

menu_key_price = ReplyKeyboardMarkup(resize_keyboard=True)
menu_key_price.row(ped, man, nar).add(menu)
