"""Скрипт для проверки файла .env"""
import os
from pathlib import Path

def check_env_file():
    """Проверка файла .env"""
    print("=" * 60)
    print("ПРОВЕРКА ФАЙЛА .env")
    print("=" * 60)
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ Файл .env не найден!")
        print("   Создайте файл .env в корне проекта")
        return False
    
    print("✅ Файл .env найден")
    
    # Загружаем переменные
    from dotenv import load_dotenv
    load_dotenv()
    
    # Проверяем обязательные параметры
    required = {
        "TELEGRAM_BOT_TOKEN": "Токен бота от @BotFather",
        "TELEGRAM_CHAT_ID": "ID группы/чата для заявок",
        "SMTP_SERVER": "SMTP сервер (например, smtp.gmail.com)",
        "SMTP_PORT": "Порт SMTP (обычно 587)",
        "SMTP_USER": "Email для отправки",
        "SMTP_PASSWORD": "Пароль приложения",
        "EMAIL_TO": "Email получателя заявок"
    }
    
    print("\nПроверка параметров:")
    print("-" * 60)
    
    all_ok = True
    for key, description in required.items():
        value = os.getenv(key)
        if value:
            # Скрываем чувствительные данные
            if "PASSWORD" in key or "TOKEN" in key:
                display_value = value[:10] + "..." if len(value) > 10 else "***"
            else:
                display_value = value
            print(f"✅ {key:20} = {display_value}")
        else:
            print(f"❌ {key:20} - не установлен")
            print(f"   {description}")
            all_ok = False
    
    # Проверяем опциональные параметры
    optional = {
        "DATABASE_URL": "sqlite:///tickets.db",
        "FILES_DIR": "files"
    }
    
    print("\nОпциональные параметры:")
    print("-" * 60)
    for key, default in optional.items():
        value = os.getenv(key, default)
        print(f"✅ {key:20} = {value}")
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ ВСЕ ПАРАМЕТРЫ НАСТРОЕНЫ ПРАВИЛЬНО!")
        print("\nСледующие шаги:")
        print("1. Установите Python 3.8+ (если еще не установлен)")
        print("2. Создайте виртуальное окружение: python -m venv venv")
        print("3. Активируйте: venv\\Scripts\\Activate.ps1")
        print("4. Установите зависимости: pip install -r requirements.txt")
        print("5. Запустите бота: python main.py")
    else:
        print("❌ НЕКОТОРЫЕ ПАРАМЕТРЫ ОТСУТСТВУЮТ")
        print("Заполните недостающие параметры в файле .env")
    print("=" * 60)
    
    return all_ok

if __name__ == "__main__":
    try:
        check_env_file()
    except ImportError:
        print("❌ Модуль python-dotenv не установлен")
        print("Установите: pip install python-dotenv")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

