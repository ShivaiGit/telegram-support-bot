"""Клавиатуры для бота"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_menu_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопками меню (можно вызвать по команде /menu)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🆕 Создать заявку"),
                KeyboardButton(text="ℹ️ Помощь")
            ],
            [
                KeyboardButton(text="❌ Отменить"),
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Главная клавиатура с основными командами"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🆕 Создать заявку"),
                KeyboardButton(text="ℹ️ Помощь")
            ],
            [
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard


def get_skip_keyboard_with_main() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой пропуска и основными командами"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭ Пропустить")],
            [
                KeyboardButton(text="🆕 Создать заявку"),
                KeyboardButton(text="ℹ️ Помощь")
            ],
            [
                KeyboardButton(text="🏠 Главное меню")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard


def get_priority_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора приоритета"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🟢 Низкий", callback_data="priority_low"),
            InlineKeyboardButton(text="🟡 Средний", callback_data="priority_medium")
        ],
        [
            InlineKeyboardButton(text="🟠 Высокий", callback_data="priority_high"),
            InlineKeyboardButton(text="🔴 Критический", callback_data="priority_critical")
        ]
    ])
    return keyboard


def get_skip_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой пропуска (устаревшая, используйте get_skip_keyboard_with_main)"""
    return get_skip_keyboard_with_main()


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для подтверждения заявки"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_yes"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="confirm_no")
        ]
    ])
    return keyboard


def get_files_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для работы с файлами"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Готово, отправить заявку", callback_data="files_done")
        ]
    ])
    return keyboard

