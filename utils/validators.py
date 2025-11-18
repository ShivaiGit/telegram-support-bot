"""Валидация данных"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """Валидация email адреса"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Валидация номера телефона"""
    if not phone:
        return False
    # Удаляем все символы кроме цифр и +
    cleaned = re.sub(r'[^\d+]', '', phone)
    # Проверяем, что осталось минимум 10 цифр
    digits = re.sub(r'[^\d]', '', cleaned)
    return len(digits) >= 10


def validate_description(description: str, max_length: int = 2000) -> bool:
    """Валидация описания проблемы"""
    if not description or not description.strip():
        return False
    return len(description) <= max_length


def clean_phone(phone: str) -> str:
    """Очистка номера телефона"""
    # Удаляем все символы кроме цифр и +
    cleaned = re.sub(r'[^\d+]', '', phone)
    return cleaned

