# Решение проблемы с установкой зависимостей

## Проблема

При установке зависимостей возникала ошибка компиляции pydantic-core, требующая Rust компилятора.

## Решение

Установите зависимости в следующем порядке:

```powershell
# 1. Установите предкомпилированные пакеты
.\venv\Scripts\pip.exe install --only-binary :all: pydantic-core
.\venv\Scripts\pip.exe install --only-binary :all: aiohttp

# 2. Установите остальные зависимости
.\venv\Scripts\pip.exe install pydantic annotated-types typing-inspection
.\venv\Scripts\pip.exe install aiogram
.\venv\Scripts\pip.exe install certifi magic-filter

# 3. Установите остальные пакеты из requirements.txt
.\venv\Scripts\pip.exe install aiosqlite python-dotenv aiofiles
```

## Альтернативный способ (если проблемы продолжаются)

Если проблемы с установкой продолжаются, используйте более новые версии:

```powershell
.\venv\Scripts\pip.exe install aiogram aiosqlite python-dotenv aiofiles --upgrade
```

Система автоматически установит совместимые версии всех зависимостей.

## Проверка установки

После установки проверьте:

```powershell
python -c "import aiogram; print('✅ aiogram работает!')"
```

Если выводится сообщение "✅ aiogram работает!", значит все установлено правильно.

## Запуск бота

```powershell
python main.py
```

