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
#### 1. Получение токена для бота и Вашего Telegram_id
```text
Пора становиться взрослыми и учиться пользоваться поиском в Вашем любимом браузере.
Этот пункт для самостоятельного изучения.
```
#### 2. Создание файла .env
```text
Создать в корневом каталоге проекта файл .env и в него внести следующие поля:
BOT_TOKEN=<Токен бота из 'BOT FATHER'> инструкция в п.2
ID_ADMIN_TELEGRAM_1=<Поле для внесения id пользователя, который будет админом > инструкция в п.2
```
#### 3.1. Запуск проекта (1 вариант)
```text
Docker
Если операционная система Windows изменить в корневом каталоге проекта файл (Dockerfile)б а именно 8 строку:
CMD [ "python3", "main.py" ]
на 
CMD [ "python", "main.py" ] 
и запустить команду ниже
```
```bash
docker-compose up -d                       
```
#### 4.2. Запуск проекта (2 вариант)
#### 4.2.1. Установка зависимостей
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### 4.2.2. Запуск проекта
```bash
python3 main.py                        
```