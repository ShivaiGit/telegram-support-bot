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
    """Валидация номера телефона (4 цифры - рабочий или 11 цифр - мобильный)"""
    if not phone:
        return False
    # Удаляем все символы кроме цифр
    digits = re.sub(r'[^\d]', '', phone)
    # Проверяем, что ровно 4 цифры (рабочий) или 11 цифр (мобильный)
    return len(digits) == 4 or len(digits) == 11


def validate_description(description: str, max_length: int = 2000) -> bool:
    """Валидация описания проблемы"""
    if not description or not description.strip():
        return False
    return len(description) <= max_length


def clean_phone(phone: str) -> str:
    """Очистка номера телефона (оставляет только цифры)"""
    # Удаляем все символы кроме цифр
    digits = re.sub(r'[^\d]', '', phone)
    # Если 11 цифр - возвращаем все, если больше - берем первые 11
    # Если 4 цифры - возвращаем все, если меньше 4 но больше 0 - берем первые 4
    if len(digits) >= 11:
        return digits[:11]
    elif len(digits) >= 4:
        return digits[:4]
    else:
        return digits

