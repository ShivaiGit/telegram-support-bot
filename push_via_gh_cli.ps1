# Альтернативный способ через GitHub CLI и прямое копирование файлов
# Использование: .\push_via_gh_cli.ps1

Write-Host "=== Альтернативная отправка через GitHub CLI ===" -ForegroundColor Cyan

$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Проверяем авторизацию
gh auth status

if ($LASTEXITCODE -ne 0) {
    Write-Host "Требуется авторизация" -ForegroundColor Red
    exit 1
}

# Создаем архив для отправки
Write-Host "`nСоздание архива..." -ForegroundColor Yellow
$archiveName = "telegram-support-bot-$(Get-Date -Format 'yyyyMMdd-HHmmss').zip"

# Исключаем ненужные файлы
$exclude = @('.git', 'files', '__pycache__', '*.pyc', '.env', '*.db', '*.log')
Get-ChildItem -Path . -Exclude $exclude | Compress-Archive -DestinationPath $archiveName -Force

Write-Host "Архив создан: $archiveName" -ForegroundColor Green
Write-Host "`nРекомендуется использовать стандартный git push после перезапуска Cursor" -ForegroundColor Yellow

