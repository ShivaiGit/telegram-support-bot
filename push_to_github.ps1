# Скрипт для отправки кода на GitHub через GitHub CLI
# Использование: .\push_to_github.ps1

Write-Host "=== Отправка кода на GitHub ===" -ForegroundColor Cyan

# Обновляем PATH для GitHub CLI
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Проверка авторизации
Write-Host "Проверка авторизации..." -ForegroundColor Yellow
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Не авторизован. Используйте: gh auth login" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Авторизация успешна" -ForegroundColor Green

# Проверяем статус git
Write-Host "`nПроверка статуса репозитория..." -ForegroundColor Yellow
git status

# Получаем список коммитов, которые нужно отправить
Write-Host "`nКоммиты для отправки:" -ForegroundColor Yellow
git log origin/main..main --oneline 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Все коммиты уже отправлены или remote не настроен" -ForegroundColor Yellow
}

# Пробуем отправить через git с явным указанием не использовать credential helper
Write-Host "`nПопытка отправки через git..." -ForegroundColor Yellow
$env:GIT_TERMINAL_PROMPT = "0"
$env:GIT_ASKPASS = ""

# Устанавливаем remote URL с токеном
$token = "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"
git remote set-url origin "https://$token@github.com/ShivaiGit/telegram-support-bot.git"

# Отправляем
Write-Host "Отправка кода..." -ForegroundColor Yellow
git -c credential.helper= push -u origin main --verbose

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Код успешно отправлен на GitHub!" -ForegroundColor Green
    Write-Host "🔗 https://github.com/ShivaiGit/telegram-support-bot" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Ошибка при отправке. Попробуйте альтернативный метод:" -ForegroundColor Red
    Write-Host "Используйте GitHub CLI для синхронизации" -ForegroundColor Yellow
}

