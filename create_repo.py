"""Скрипт для создания репозитория на GitHub через API"""
import requests
import subprocess
import sys
import os

GITHUB_USERNAME = "ShivaiGit"
REPO_NAME = "telegram-support-bot"

def create_repo_with_token(token):
    """Создание репозитория через GitHub API с токеном"""
    url = f"https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO_NAME,
        "description": "Telegram-бот для автоматизации приема и распределения заявок в отдел технической поддержки",
        "public": True,
        "auto_init": False
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print("✅ Репозиторий успешно создан!")
        return True
    else:
        print(f"❌ Ошибка: {response.status_code}")
        print(response.json())
        return False

def setup_remote_and_push():
    """Настройка remote и отправка кода"""
    try:
        # Проверяем, есть ли уже remote
        result = subprocess.run(["git", "remote", "get-url", "origin"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Remote 'origin' уже настроен")
        else:
            # Добавляем remote
            repo_url = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
            print("✅ Remote 'origin' добавлен")
        
        # Отправляем код
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        print("✅ Код успешно отправлен на GitHub!")
        print(f"🔗 Ссылка: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при отправке кода: {e}")
        return False

if __name__ == "__main__":
    # Проверяем токен в переменной окружения или аргументах
    token = os.getenv("GITHUB_TOKEN")
    
    if not token and len(sys.argv) > 1:
        token = sys.argv[1]
    
    if not token:
        print("Использование:")
        print("  python create_repo.py <GITHUB_TOKEN>")
        print("  или")
        print("  $env:GITHUB_TOKEN='your_token'; python create_repo.py")
        print("\nСоздайте токен на: https://github.com/settings/tokens/new")
        print("Нужны права: repo")
        sys.exit(1)
    
    if create_repo_with_token(token):
        setup_remote_and_push()

