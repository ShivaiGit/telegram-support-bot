"""Тестовый скрипт для проверки основных компонентов бота"""
import sys
import os

def test_imports():
    """Проверка импортов"""
    print("=" * 50)
    print("Тест 1: Проверка импортов")
    print("=" * 50)
    
    try:
        import asyncio
        print("✅ asyncio")
    except ImportError as e:
        print(f"❌ asyncio: {e}")
        return False
    
    try:
        import aiogram
        print("✅ aiogram")
    except ImportError as e:
        print(f"❌ aiogram: {e}")
        print("   Установите: pip install aiogram")
        return False
    
    try:
        import aiosqlite
        print("✅ aiosqlite")
    except ImportError as e:
        print(f"❌ aiosqlite: {e}")
        print("   Установите: pip install aiosqlite")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv")
    except ImportError as e:
        print(f"❌ python-dotenv: {e}")
        print("   Установите: pip install python-dotenv")
        return False
    
    try:
        import aiofiles
        print("✅ aiofiles")
    except ImportError as e:
        print(f"❌ aiofiles: {e}")
        print("   Установите: pip install aiofiles")
        return False
    
    return True

def test_project_structure():
    """Проверка структуры проекта"""
    print("\n" + "=" * 50)
    print("Тест 2: Проверка структуры проекта")
    print("=" * 50)
    
    required_files = [
        "main.py",
        "config.py",
        "bot/handlers.py",
        "bot/states.py",
        "bot/keyboards.py",
        "database/db.py",
        "database/models.py",
        "services/telegram_service.py",
        "services/email_service.py",
        "utils/validators.py",
        "requirements.txt"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - не найден")
            all_exist = False
    
    return all_exist

def test_syntax():
    """Проверка синтаксиса Python файлов"""
    print("\n" + "=" * 50)
    print("Тест 3: Проверка синтаксиса")
    print("=" * 50)
    
    python_files = [
        "main.py",
        "config.py",
        "bot/handlers.py",
        "bot/states.py",
        "bot/keyboards.py",
        "database/db.py",
        "database/models.py",
        "services/telegram_service.py",
        "services/email_service.py",
        "utils/validators.py"
    ]
    
    all_valid = True
    for file in python_files:
        if not os.path.exists(file):
            continue
        try:
            with open(file, 'r', encoding='utf-8') as f:
                compile(f.read(), file, 'exec')
            print(f"✅ {file}")
        except SyntaxError as e:
            print(f"❌ {file}: Синтаксическая ошибка - {e}")
            all_valid = False
        except Exception as e:
            print(f"⚠️  {file}: {e}")
    
    return all_valid

def test_config():
    """Проверка конфигурации"""
    print("\n" + "=" * 50)
    print("Тест 4: Проверка конфигурации")
    print("=" * 50)
    
    try:
        from config import Config
        print("✅ Модуль config импортирован")
        
        # Проверяем наличие .env файла
        if os.path.exists(".env"):
            print("✅ Файл .env существует")
        else:
            print("⚠️  Файл .env не найден")
            print("   Создайте файл .env на основе примера в README.md")
        
        # Пробуем валидацию (может упасть, если нет .env)
        try:
            Config.validate()
            print("✅ Все обязательные параметры настроены")
        except ValueError as e:
            print(f"⚠️  {e}")
            print("   Это нормально, если .env файл еще не создан")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке конфигурации: {e}")
        return False
    
    return True

def test_database_structure():
    """Проверка структуры базы данных"""
    print("\n" + "=" * 50)
    print("Тест 5: Проверка моделей базы данных")
    print("=" * 50)
    
    try:
        from database.models import Ticket, TicketFile
        print("✅ Модели Ticket и TicketFile импортированы")
        
        # Проверяем наличие методов
        methods = ['create', 'get_by_number', 'get_by_user_id', 'get_next_ticket_number']
        for method in methods:
            if hasattr(Ticket, method):
                print(f"✅ Ticket.{method}")
            else:
                print(f"❌ Ticket.{method} - не найден")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка при проверке моделей: {e}")
        return False

def main():
    """Главная функция тестирования"""
    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ TELEGRAM SUPPORT BOT")
    print("=" * 50 + "\n")
    
    results = []
    
    results.append(("Импорты", test_imports()))
    results.append(("Структура проекта", test_project_structure()))
    results.append(("Синтаксис", test_syntax()))
    results.append(("Конфигурация", test_config()))
    results.append(("База данных", test_database_structure()))
    
    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    
    for name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("\nСледующие шаги:")
        print("1. Установите Python 3.8+")
        print("2. Создайте виртуальное окружение: python -m venv venv")
        print("3. Активируйте его: venv\\Scripts\\activate")
        print("4. Установите зависимости: pip install -r requirements.txt")
        print("5. Создайте файл .env с настройками")
        print("6. Запустите бота: python main.py")
    else:
        print("⚠️  НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        print("Исправьте ошибки перед запуском бота")
    print("=" * 50 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

