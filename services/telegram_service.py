"""Сервис для отправки сообщений в Telegram"""
from typing import List, Optional
from aiogram import Bot
from config import Config
from database.models import Ticket, TicketFile
import pytz


async def send_ticket_to_chat(bot: Bot, ticket: Ticket, files: Optional[List[TicketFile]] = None):
    """Отправка заявки в рабочий чат"""
    files = files or []
    
    # Формирование сообщения
    priority_emoji = {
        "low": "🟢",
        "medium": "🟡",
        "high": "🟠",
        "critical": "🔴"
    }
    
    priority_text = {
        "low": "Низкий",
        "medium": "Средний",
        "high": "Высокий",
        "critical": "Критический"
    }
    
    # Форматирование времени с учетом часового пояса
    moscow_tz = pytz.timezone("Europe/Moscow")
    if ticket.created_at:
        if ticket.created_at.tzinfo is None:
            # Если время без часового пояса, считаем его московским
            dt = moscow_tz.localize(ticket.created_at)
        else:
            # Конвертируем в московское время
            dt = ticket.created_at.astimezone(moscow_tz)
        date_str = dt.strftime('%d.%m.%Y %H:%M')
    else:
        date_str = 'Не указано'
    
    message = f"""🔔 Новая заявка {ticket.ticket_number}

👤 Пользователь: {ticket.username or 'Не указано'}
📞 Телефон: {ticket.phone}
📧 Email: {ticket.email or 'Не указано'}
📍 Местонахождение: {ticket.location or 'Не указано'}
📅 Дата: {date_str}
⚡ Приоритет: {priority_emoji.get(ticket.priority, '🟡')} {priority_text.get(ticket.priority, 'Средний')}

📝 Описание:
{ticket.description}"""
    
    if files:
        message += f"\n\n📎 Вложения: {len(files)} файл(ов)"
    
    try:
        # Отправка текстового сообщения
        await bot.send_message(
            chat_id=Config.TELEGRAM_CHAT_ID,
            text=message
        )
        
        # Отправка файлов, если есть
        for file_info in files:
            try:
                if file_info.file_type == "photo":
                    await bot.send_photo(
                        chat_id=Config.TELEGRAM_CHAT_ID,
                        photo=file_info.file_id
                    )
                else:
                    await bot.send_document(
                        chat_id=Config.TELEGRAM_CHAT_ID,
                        document=file_info.file_id
                    )
            except Exception as e:
                # Логируем ошибку, но продолжаем отправку других файлов
                print(f"Ошибка при отправке файла {file_info.file_id}: {e}")
    
    except Exception as e:
        print(f"Ошибка при отправке заявки в чат: {e}")
        raise

