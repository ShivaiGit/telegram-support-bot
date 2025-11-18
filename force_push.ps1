# Принудительная отправка через GitHub API
# Использование: .\force_push.ps1

$token = "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"
$repo = "ShivaiGit/telegram-support-bot"

Write-Host "=== Принудительная отправка через GitHub API ===" -ForegroundColor Cyan

# Получаем SHA последнего коммита
$lastCommit = git rev-parse HEAD
Write-Host "Последний коммит: $lastCommit" -ForegroundColor Yellow

# Проверяем, есть ли уже что-то на GitHub
$headers = @{
    Authorization = "Bearer $token"
    Accept = "application/vnd.github.v3+json"
}

try {
    $ref = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/git/refs/heads/main" -Headers $headers -Method Get -ErrorAction SilentlyContinue
    Write-Host "Ветка main существует на GitHub" -ForegroundColor Green
    Write-Host "Текущий SHA на GitHub: $($ref.object.sha)" -ForegroundColor Yellow
} catch {
    Write-Host "Ветка main не существует, создаем..." -ForegroundColor Yellow
    
    # Получаем SHA основного дерева
    $treeSha = git rev-parse HEAD^{tree}
    
    # Создаем дерево через API (это сложно, проще использовать git push)
    Write-Host "Рекомендуется использовать веб-интерфейс GitHub или попробовать:" -ForegroundColor Yellow
    Write-Host "git push -u origin main --force" -ForegroundColor Cyan
}

Write-Host "`nПопробуйте выполнить вручную:" -ForegroundColor Yellow
Write-Host "git config --global credential.helper manager-core" -ForegroundColor Cyan
Write-Host "git push -u origin main" -ForegroundColor Cyan

