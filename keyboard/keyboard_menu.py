from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# стартовое меню для пользователя
application = KeyboardButton("Записаться")
price = KeyboardButton("Цены")
contacts = KeyboardButton("Контакты")

main_menu_user = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_user.row(application, price).add(contacts)


# стартовое меню для админа
admin = KeyboardButton("Админ_панель")
main_menu_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_admin.row(application, price, contacts).add(admin)

# меню админа
all_user = KeyboardButton("Пользователи")
all_applications = KeyboardButton("Заказы")
message_all = KeyboardButton("Отправить сообщение всем пользователям бота")

menu_back = KeyboardButton("Возврат в меню")

admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu.row(all_user, all_applications).add(message_all).add(menu_back)
