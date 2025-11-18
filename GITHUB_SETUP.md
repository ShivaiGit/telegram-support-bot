# Инструкция по настройке GitHub репозитория

## Шаги для подключения к GitHub:

1. **Создайте новый репозиторий на GitHub:**
   - Перейдите на https://github.com/new
   - Введите название репозитория (например: `telegram-support-bot`)
   - Выберите Public или Private
   - **НЕ** создавайте README, .gitignore или лицензию (они уже есть)
   - Нажмите "Create repository"

2. **Подключите локальный репозиторий к GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/telegram-support-bot.git
   ```
   Замените `YOUR_USERNAME` на ваш GitHub username

3. **Отправьте код на GitHub:**
   ```bash
   git branch -M main
   git push -u origin main
   ```

## Альтернативный способ (через SSH):

Если у вас настроен SSH ключ:
```bash
git remote add origin git@github.com:YOUR_USERNAME/telegram-support-bot.git
git branch -M main
git push -u origin main
```

## После настройки:

Все последующие изменения можно пушить командой:
```bash
git add .
git commit -m "Описание изменений"
git push
```

