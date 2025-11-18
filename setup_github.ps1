# Скрипт для настройки GitHub репозитория
# Использование: .\setup_github.ps1

# Обновляем PATH для GitHub CLI
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "Проверка авторизации GitHub..." -ForegroundColor Yellow
$authStatus = gh auth status 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "Требуется авторизация. Запускаю процесс авторизации..." -ForegroundColor Yellow
    gh auth login --web
    Write-Host "После завершения авторизации нажмите Enter..." -ForegroundColor Green
    Read-Host
}

Write-Host "Создание репозитория на GitHub..." -ForegroundColor Yellow
gh repo create telegram-support-bot --public --source=. --remote=origin --push

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Репозиторий успешно создан и код отправлен!" -ForegroundColor Green
    Write-Host "Ссылка на репозиторий: https://github.com/ShivaiGit/telegram-support-bot" -ForegroundColor Cyan
} else {
    Write-Host "❌ Ошибка при создании репозитория" -ForegroundColor Red
}

