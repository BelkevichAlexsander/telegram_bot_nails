import sqlite3 as sq

base = sq.connect('f.db')
cur = base.cursor()


def sql_start():
    """
    Подключение к бд и создание таблиц users, applications если такие не созданы
    :return: None
    """
    if base:
        print('data base connect')
    base.execute('CREATE TABLE IF NOT EXISTS users'
                 '(id INTEGER PRIMARY KEY UNIQUE, '
                 'full_name TEXT,'
                 'status_in_menu TEXT)'
                 )
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS applications'
                 '(full_name TEXT,'
                 'service TEXT,'
                 'date TEXT,'
                 'time TEXT,'
                 'number TEXT,'
                 'id_user INT UNIQUE'
                 'FOREIGN KEY id_user REFERENCES user (id))'
                 )
    base.commit()


async def sql_add_user(state: tuple):
    """
    Добавление пользователя в бд, когда тот вызывает меню у бота
    :param state: tuple(id: int, full_name: str, status_in_menu: str)
    :return: None
    """
    cur.execute('INSERT OR REPLACE INTO users VALUES (?, ?, ?)', state)
    base.commit()


async def all_users(status: str):
    """
    Выборка всей таблицы users
    :param status: String
    :return: None
    """
    return cur.execute(f'SELECT * FROM users WHERE status_in_menu = ?', (status, )).fetchall()


async def applications_date() -> list:
    """
    Получение одного элемента по индефикатору из таблицы users
    :return: List(Tuple(all columns), ..., Tuple(all columns))
    """
    return cur.execute(f'SELECT * FROM applications').fetchall()


async def sql_add_application(date: tuple):
    """
    Добавление заявки в бд
    :param date: Tuple(full_name: str, service: str, date: str, time: str, id_user: str, number: str)
    :return: None
    """
    cur.execute('INSERT INTO applications VALUES (?, ?, ?, ?, ?, ?)', date)
    base.commit()


async def select_date_application(date: str) -> list:
    """
    Получение списка занятых дат
    :param date: String
    :return: List(Tuple(time: str), ..., Tuple(time: str))
    """
    return cur.execute(f'SELECT time FROM applications WHERE date = ?',
                       (date, )).fetchall()
