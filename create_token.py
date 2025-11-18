"""Скрипт для создания GitHub токена через API"""
import requests
import base64
import json

username = "ShivaiGit"
password = "Buldozerfx6100"

# GitHub больше не поддерживает создание токенов через API с паролем
# Нужно использовать веб-интерфейс или OAuth

print("GitHub больше не поддерживает создание токенов через API с паролем.")
print("Необходимо создать токен вручную:")
print("1. Перейдите на: https://github.com/settings/tokens/new")
print("2. Введите название: telegram-bot-deploy")
print("3. Выберите права: repo (все права репозиториев)")
print("4. Нажмите 'Generate token'")
print("5. Скопируйте токен и используйте его для авторизации")

