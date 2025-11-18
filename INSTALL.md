# Инструкция по установке и запуску

## Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

## Установка

### 1. Установите Python

**Windows:**
- Скачайте Python с официального сайта: https://www.python.org/downloads/
- При установке обязательно отметьте "Add Python to PATH"
- Или установите через Microsoft Store

**Проверка установки:**
```bash
python --version
# или
py --version
```

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
```

### 3. Активируйте виртуальное окружение

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Установите зависимости

```bash
pip install -r requirements.txt
```

### 5. Создайте файл .env

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_work_chat_id_here

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_TO=support@company.com

# Database Configuration
DATABASE_URL=sqlite:///tickets.db

# Files Storage
FILES_DIR=files
```

### 6. Получите токен бота

1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в файл `.env`

### 7. Получите ID рабочего чата

1. Добавьте бота в групповой чат
2. Отправьте любое сообщение в чат
3. Откройте в браузере: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Найдите `"chat":{"id":-123456789}` - это и есть ваш `TELEGRAM_CHAT_ID`

### 8. Настройте email (для Gmail)

1. Включите двухфакторную аутентификацию
2. Создайте пароль приложения: https://myaccount.google.com/apppasswords
3. Используйте этот пароль в `SMTP_PASSWORD`

## Запуск

### Тестирование

Сначала проверьте, что все работает:

```bash
python test_bot.py
```

### Запуск бота

```bash
python main.py
```

Бот должен запуститься и начать отвечать на команды в Telegram.

## Команды бота

- `/start` - приветствие и начало работы
- `/help` - справка по использованию
- `/new` - создать новую заявку
- `/cancel` - отменить текущую операцию

## Устранение неполадок

### Ошибка "Python was not found"

Установите Python и убедитесь, что он добавлен в PATH.

### Ошибка "ModuleNotFoundError"

Убедитесь, что виртуальное окружение активировано и зависимости установлены:
```bash
pip install -r requirements.txt
```

### Ошибка конфигурации

Проверьте, что файл `.env` создан и содержит все обязательные параметры.

### Бот не отвечает

1. Проверьте, что токен бота правильный
2. Убедитесь, что бот запущен (`python main.py`)
3. Проверьте логи на наличие ошибок

