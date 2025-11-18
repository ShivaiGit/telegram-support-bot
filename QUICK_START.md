# Быстрый старт

## 1. Установите Python

Скачайте и установите Python 3.8+ с https://www.python.org/downloads/
**Важно:** При установке отметьте "Add Python to PATH"

## 2. Установите зависимости

Откройте терминал в папке проекта и выполните:

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его (Windows PowerShell)
venv\Scripts\Activate.ps1

# Установите зависимости
pip install -r requirements.txt
```

## 3. Создайте файл .env

Создайте файл `.env` в корне проекта:

```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_CHAT_ID=id_вашего_чата
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=ваш_email@gmail.com
SMTP_PASSWORD=пароль_приложения
EMAIL_TO=support@company.com
```

## 4. Запустите бота

```bash
python main.py
```

## Тестирование без запуска

Проверьте код на ошибки:

```bash
python test_bot.py
```

## Полная инструкция

См. файл `INSTALL.md` для подробной инструкции.

