"""Сервис для отправки email"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import aiofiles
import os
from config import Config
from database.models import Ticket, TicketFile
from zoneinfo import ZoneInfo


async def send_ticket_to_email(ticket: Ticket, files: Optional[List[TicketFile]] = None):
    """Отправка заявки на email"""
    files = files or []
    
    # Формирование темы письма
    priority_text = {
        "low": "Низкий",
        "medium": "Средний",
        "high": "Высокий",
        "critical": "Критический"
    }
    
    description_preview = ticket.description[:50] + "..." if len(ticket.description) > 50 else ticket.description
    subject = f"[Техподдержка] Заявка {ticket.ticket_number} - {description_preview}"
    
    # Форматирование времени с учетом часового пояса
    moscow_tz = ZoneInfo("Europe/Moscow")
    if ticket.created_at:
        if ticket.created_at.tzinfo is None:
            # Если время без часового пояса, считаем его московским
            dt = ticket.created_at.replace(tzinfo=moscow_tz)
        else:
            # Конвертируем в московское время
            dt = ticket.created_at.astimezone(moscow_tz)
        date_str = dt.strftime('%d.%m.%Y %H:%M')
    else:
        date_str = 'Не указано'
    
    # Формирование тела письма
    body = f"""Здравствуйте!

Поступила новая заявка в отдел технической поддержки.

Номер заявки: {ticket.ticket_number}
Дата создания: {date_str}
Приоритет: {priority_text.get(ticket.priority, 'Средний')}

Данные пользователя:
- Имя: {ticket.username or 'Не указано'}
- Телефон: {ticket.phone}
- Email: {ticket.email or 'Не указано'}
- Местонахождение: {ticket.location or 'Не указано'}

Описание проблемы:
{ticket.description}

"""
    
    if files:
        body += f"К заявке прикреплены файлы (см. вложения).\n\n"
    
    body += "---\nЭто автоматическое сообщение от Telegram-бота техподдержки."
    
    try:
        # Создание сообщения
        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_USER
        msg['To'] = Config.EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Добавление вложений
        for file_info in files:
            if file_info.file_path and os.path.exists(file_info.file_path):
                try:
                    async with aiofiles.open(file_info.file_path, 'rb') as f:
                        file_data = await f.read()
                    
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file_data)
                    encoders.encode_base64(part)
                    
                    filename = os.path.basename(file_info.file_path)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {filename}'
                    )
                    msg.attach(part)
                except Exception as e:
                    print(f"Ошибка при добавлении файла {file_info.file_path}: {e}")
        
        # Отправка письма
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.starttls()
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"Заявка {ticket.ticket_number} успешно отправлена на email")
    
    except Exception as e:
        print(f"Ошибка при отправке заявки на email: {e}")
        raise

