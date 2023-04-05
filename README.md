### Telegram-bot
#### 0. Описание задания
```text
Меню
У бота для пользователя три основные кнопки(keyboard) меню:

     1. Записаться. 
        При нажатии на эту кнопку, выводятся кнопки(inline) с вариантами услуг. 
        Выбор даты в виде календаря кнопки(inline).
        Выбор времени в виде кнопок(inline). (несколько записей на один день и одно и тоже время невозможно)
        Поделиться контактом или ввести номер.
        После чего данная заявка со всеми выборами и номером отправляться админу.
    
     2. Цены.
        2.1. Педикюр.
        2.2. Маникюр.
        2.3. Наращивание.
             P.S.Каждая кнопка выводит сообщения о стоимости выбранной услуги. 
        2.4. Возврат в меню.    
        
     3. Контакты. 
        Информация об адресе и контактном телефоне.
       
Функции админа:
     У админа помимо основного функционала есть кнопка в основном меню:
         4. Админ_панель.
            4.1. Пользователи.
                 Вывод из бд всех пользователей.
            4.2. Заказы.
                 Вывод из бд всех заказов.
            4.3. Отправить сообщение всем пользователям бота.
```
#### 1. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### 2. Получение токенов для бота и системы оплаты, а также Вашего Telegram_id и заполнение файла .env
```text
Пора становиться взрослыми и учиться пользоваться поиском в Вашем любимом браузере.
Этот пункт для самостоятельного изучения.
```
#### 3. Запуск проекта
```text
Создать файл .env и вснего внести поля
BOT_TOKEN="<Токен бота из 'BOT FATHER'>"
ID_ADMIN_TELEGRAM_1=<Поле для внесения id пользователя, который будет админом >
```
```bash
python3 main.py                        
```