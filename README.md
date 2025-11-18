# Telegram Support Bot

Telegram-бот для автоматизации приема и распределения заявок в отдел технической поддержки.

## Описание

Бот принимает заявки от пользователей через Telegram, сохраняет их в базу данных и автоматически пересылает в рабочий чат и на электронную почту отдела технической поддержки.

## Возможности

- ✅ Прием заявок от пользователей через Telegram
- ✅ Сбор информации: имя, телефон, email, описание проблемы, приоритет
- ✅ Прикрепление файлов (фото, документы, скриншоты)
- ✅ Автоматическая отправка заявок в Telegram чат
- ✅ Автоматическая отправка заявок на email
- ✅ Уникальные номера заявок для отслеживания
- ✅ Валидация данных

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/telegram-support-bot.git
cd telegram-support-bot
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл и укажите свои данные
```

5. Запустите бота:
```bash
python main.py
```

## Конфигурация

Создайте файл `.env` на основе `.env.example` и заполните следующие параметры:

- `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота (получить у @BotFather)
- `TELEGRAM_CHAT_ID` - ID рабочего чата для получения заявок
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - настройки SMTP сервера
- `EMAIL_TO` - email адрес отдела техподдержки
- `DATABASE_URL` - URL базы данных (по умолчанию SQLite)

## Команды бота

- `/start` - приветствие и начало работы
- `/help` - справка по использованию
- `/new` - создать новую заявку
- `/cancel` - отменить текущую операцию

## Структура проекта

```
telegram-support-bot/
├── bot/
│   ├── __init__.py
│   ├── handlers.py      # Обработчики команд и сообщений
│   ├── states.py        # Состояния FSM
│   └── keyboards.py     # Клавиатуры
├── database/
│   ├── __init__.py
│   ├── models.py        # Модели базы данных
│   └── db.py            # Работа с БД
├── services/
│   ├── __init__.py
│   ├── email_service.py # Отправка email
│   └── telegram_service.py # Отправка в чат
├── utils/
│   ├── __init__.py
│   └── validators.py    # Валидация данных
├── files/               # Хранилище файлов
├── main.py             # Точка входа
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
└── README.md          # Документация
```

## Разработка

Проект разработан на Python 3.8+ с использованием:
- `aiogram` - асинхронный фреймворк для Telegram Bot API
- `aiosqlite` - асинхронная работа с SQLite
- `python-dotenv` - управление переменными окружения

## Лицензия

MIT

