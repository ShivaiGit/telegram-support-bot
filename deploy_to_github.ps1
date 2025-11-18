# Скрипт для отправки кода на GitHub
# Использование: .\deploy_to_github.ps1

Write-Host "=== Развертывание проекта на GitHub ===" -ForegroundColor Cyan
Write-Host ""

# Обновляем PATH для GitHub CLI
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Проверка авторизации
Write-Host "Проверка авторизации GitHub..." -ForegroundColor Yellow
$authCheck = gh auth status 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Не авторизован в GitHub CLI" -ForegroundColor Red
    Write-Host ""
    Write-Host "Варианты авторизации:" -ForegroundColor Yellow
    Write-Host "1. Веб-авторизация: gh auth login --web" -ForegroundColor Cyan
    Write-Host "2. С токеном: `$env:GH_TOKEN='your_token'; gh auth login --with-token" -ForegroundColor Cyan
    Write-Host ""
    
    $choice = Read-Host "Запустить веб-авторизацию? (y/n)"
    if ($choice -eq "y" -or $choice -eq "Y") {
        Write-Host "Откройте браузер и завершите авторизацию..." -ForegroundColor Yellow
        gh auth login --web
        Write-Host "Нажмите Enter после завершения авторизации..." -ForegroundColor Green
        Read-Host
    } else {
        Write-Host "Для продолжения нужна авторизация. Выход." -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ Авторизация успешна!" -ForegroundColor Green
Write-Host ""

# Проверяем, существует ли репозиторий
Write-Host "Проверка существования репозитория..." -ForegroundColor Yellow
$repoCheck = gh repo view ShivaiGit/telegram-support-bot 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Репозиторий уже существует" -ForegroundColor Green
    Write-Host "Настройка remote и отправка кода..." -ForegroundColor Yellow
    
    # Проверяем remote
    $remoteCheck = git remote get-url origin 2>&1
    if ($LASTEXITCODE -ne 0) {
        git remote add origin https://github.com/ShivaiGit/telegram-support-bot.git
        Write-Host "✅ Remote 'origin' добавлен" -ForegroundColor Green
    }
    
    # Отправляем код
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Код успешно отправлен на GitHub!" -ForegroundColor Green
        Write-Host "🔗 https://github.com/ShivaiGit/telegram-support-bot" -ForegroundColor Cyan
    }
} else {
    Write-Host "Создание нового репозитория..." -ForegroundColor Yellow
    gh repo create telegram-support-bot --public --source=. --remote=origin --push
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Репозиторий создан и код отправлен!" -ForegroundColor Green
        Write-Host "🔗 https://github.com/ShivaiGit/telegram-support-bot" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Ошибка при создании репозитория" -ForegroundColor Red
    }
}

