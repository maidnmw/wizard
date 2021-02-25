# Wizard

## DB
Запустить docker-compose up

## Backend
1. Настроить виртуальное окружение
2. Зайти в виртуальное окружение source .venv/bin/activate
3. Установить необходимые зависимости pip install -r requirements.txt
4. Провести миграции python manage.py migrate
5. Запустить python manage.py runserver 0.0.0.0:8080

**ВАЖНО!!!** Не забываем фризить установленные зависимости pip freeze > requirements.txt

## Frontend
1. Установить необходимые зависимости npm i
2. Запустить
- Сервер для разработки npm run dev
- Продакшн сервер npm run build -> npm run start
