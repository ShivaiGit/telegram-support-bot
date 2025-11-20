"""Обработчики команд и сообщений бота"""
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
import aiofiles
from config import Config
from database.models import Ticket, TicketFile
from database.db import init_db
from bot.states import TicketForm
from bot.keyboards import (
    get_priority_keyboard,
    get_confirm_keyboard,
    get_files_keyboard
)
from utils.validators import validate_email, validate_phone, validate_description, clean_phone
from services.telegram_service import send_ticket_to_chat
from services.email_service import send_ticket_to_email

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Хранилище временных данных заявки
ticket_data = {}


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Обработчик команды /start"""
    await state.clear()
    welcome_text = """👋 Добро пожаловать в бот технической поддержки!

Я помогу вам создать заявку для отдела технической поддержки.

Доступные команды:
/new - создать новую заявку
/help - справка
/cancel - отменить текущую операцию"""
    
    await message.answer(welcome_text)


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = """📖 Справка по использованию бота

Для создания заявки используйте команду /new

Бот запросит у вас следующую информацию:
• Имя (обязательно)
• Телефон (обязательно)
• Email (обязательно)
• Местонахождение (обязательно)
• Описание проблемы (обязательно)
• Приоритет заявки
• Файлы (необязательно)

После заполнения всех данных вы сможете просмотреть сводку и подтвердить отправку заявки.

Команды:
/new - создать новую заявку
/cancel - отменить текущую операцию
/help - показать эту справку"""
    
    await message.answer(help_text)


@router.message(Command("new"))
async def cmd_new(message: Message, state: FSMContext):
    """Обработчик команды /new - начало создания заявки"""
    await state.clear()
    await state.set_state(TicketForm.waiting_for_name)
    await message.answer(
        "📝 Начнем создание новой заявки!\n\n"
        "Пожалуйста, введите ваше имя:"
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Обработчик команды /cancel"""
    await state.clear()
    await message.answer("❌ Операция отменена. Используйте /new для создания новой заявки.")


@router.message(StateFilter(TicketForm.waiting_for_name))
async def process_name(message: Message, state: FSMContext):
    """Обработка имени пользователя"""
    name = message.text.strip()
    
    if not name or len(name) < 2:
        await message.answer("❌ Имя должно содержать минимум 2 символа. Попробуйте еще раз:")
        return
    
    await state.update_data(name=name)
    await state.set_state(TicketForm.waiting_for_phone)
    await message.answer(
        f"✅ Имя сохранено: {name}\n\n"
        "Теперь введите ваш контактный телефон:"
    )


@router.message(StateFilter(TicketForm.waiting_for_phone))
async def process_phone(message: Message, state: FSMContext):
    """Обработка телефона"""
    phone = message.text.strip()
    cleaned_phone = clean_phone(phone)
    
    if not validate_phone(cleaned_phone):
        await message.answer(
            "❌ Некорректный формат телефона. Пожалуйста, введите номер телефона еще раз:"
        )
        return
    
    await state.update_data(phone=cleaned_phone)
    await state.set_state(TicketForm.waiting_for_email)
    await message.answer(
        f"✅ Телефон сохранен: {cleaned_phone}\n\n"
        "Введите ваш email адрес:"
    )


@router.message(StateFilter(TicketForm.waiting_for_email))
async def process_email(message: Message, state: FSMContext):
    """Обработка email"""
    email = message.text.strip()
    
    if not validate_email(email):
        await message.answer(
            "❌ Некорректный формат email. Пожалуйста, введите корректный email адрес:"
        )
        return
    
    await state.update_data(email=email)
    await state.set_state(TicketForm.waiting_for_location)
    await message.answer(
        f"✅ Email сохранен: {email}\n\n"
        "Укажите ваше местонахождение (город, адрес или другое):"
    )


@router.message(StateFilter(TicketForm.waiting_for_location))
async def process_location(message: Message, state: FSMContext):
    """Обработка местонахождения"""
    location = message.text.strip()
    
    if not location or len(location) < 2:
        await message.answer(
            "❌ Местонахождение должно содержать минимум 2 символа. Попробуйте еще раз:"
        )
        return
    
    await state.update_data(location=location)
    await state.set_state(TicketForm.waiting_for_description)
    await message.answer(
        f"✅ Местонахождение сохранено: {location}\n\n"
        "Теперь опишите вашу проблему подробно:"
    )


@router.message(StateFilter(TicketForm.waiting_for_description))
async def process_description(message: Message, state: FSMContext):
    """Обработка описания проблемы"""
    description = message.text.strip()
    
    if not validate_description(description):
        await message.answer(
            "❌ Описание не может быть пустым и не должно превышать 2000 символов. "
            "Попробуйте еще раз:"
        )
        return
    
    await state.update_data(description=description)
    await state.set_state(TicketForm.waiting_for_priority)
    await message.answer(
        f"✅ Описание сохранено\n\n"
        "Выберите приоритет заявки:",
        reply_markup=get_priority_keyboard()
    )


@router.callback_query(StateFilter(TicketForm.waiting_for_priority), F.data.startswith("priority_"))
async def process_priority(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора приоритета"""
    priority = callback.data.split("_")[1]
    priority_names = {
        "low": "Низкий",
        "medium": "Средний",
        "high": "Высокий",
        "critical": "Критический"
    }
    
    await state.update_data(priority=priority)
    await state.set_state(TicketForm.waiting_for_files)
    await state.update_data(files=[])
    
    await callback.message.edit_text(
        f"✅ Приоритет выбран: {priority_names.get(priority, priority)}\n\n"
        "Теперь вы можете прикрепить файлы (фото, документы, скриншоты).\n"
        "Отправьте файлы по одному или нажмите 'Готово', чтобы пропустить:",
        reply_markup=get_files_keyboard()
    )
    await callback.answer()


@router.message(StateFilter(TicketForm.waiting_for_files), F.photo | F.document)
async def process_file(message: Message, state: FSMContext):
    """Обработка прикрепленных файлов"""
    data = await state.get_data()
    files = data.get("files", [])
    
    # Создаем директорию для файлов, если её нет
    os.makedirs(Config.FILES_DIR, exist_ok=True)
    
    file_id = None
    file_type = None
    file_path = None
    
    if message.photo:
        # Обработка фото
        photo = message.photo[-1]  # Берем фото наибольшего размера
        file_id = photo.file_id
        file_type = "photo"
        file_info = await message.bot.get_file(file_id)
        file_path = os.path.join(Config.FILES_DIR, f"{file_id}.jpg")
        
        # Скачиваем файл
        await message.bot.download_file(file_info.file_path, file_path)
    
    elif message.document:
        # Обработка документа
        document = message.document
        file_id = document.file_id
        file_type = "document"
        file_info = await message.bot.get_file(file_id)
        file_path = os.path.join(Config.FILES_DIR, document.file_name or f"{file_id}")
        
        # Скачиваем файл
        await message.bot.download_file(file_info.file_path, file_path)
    
    if file_id:
        files.append({
            "file_id": file_id,
            "file_type": file_type,
            "file_path": file_path
        })
        await state.update_data(files=files)
        await message.answer(f"✅ Файл добавлен ({len(files)} файл(ов))")


@router.callback_query(StateFilter(TicketForm.waiting_for_files), F.data == "files_done")
async def files_done(callback: CallbackQuery, state: FSMContext):
    """Завершение добавления файлов"""
    data = await state.get_data()
    files = data.get("files", [])
    
    await state.set_state(TicketForm.confirming)
    
    # Формируем сводку заявки
    summary = f"""📋 Сводка заявки:

👤 Имя: {data.get('name')}
📞 Телефон: {data.get('phone')}
📧 Email: {data.get('email') or 'Не указано'}
📍 Местонахождение: {data.get('location', 'Не указано')}
📝 Описание: {data.get('description')[:100]}{'...' if len(data.get('description', '')) > 100 else ''}
⚡ Приоритет: {data.get('priority', 'medium')}
📎 Файлов: {len(files)}

Проверьте данные и подтвердите отправку заявки:"""
    
    await callback.message.edit_text(summary, reply_markup=get_confirm_keyboard())
    await callback.answer()


@router.callback_query(StateFilter(TicketForm.confirming), F.data == "confirm_yes")
async def confirm_ticket(callback: CallbackQuery, state: FSMContext):
    """Подтверждение и создание заявки"""
    data = await state.get_data()
    
    try:
        # Генерируем номер заявки на основе ID пользователя
        ticket_number = await Ticket.get_next_ticket_number(callback.from_user.id)
        
        # Создаем заявку в БД
        ticket = await Ticket.create(
            ticket_number=ticket_number,
            user_id=callback.from_user.id,
            username=data.get('name'),
            phone=data.get('phone'),
            email=data.get('email'),
            location=data.get('location'),
            description=data.get('description'),
            priority=data.get('priority', 'medium')
        )
        
        # Сохраняем файлы
        files_data = data.get('files', [])
        ticket_files = []
        for file_data in files_data:
            file_record = await TicketFile.create(
                ticket_id=ticket.id,
                file_id=file_data['file_id'],
                file_type=file_data['file_type'],
                file_path=file_data['file_path']
            )
            ticket_files.append(file_record)
        
        # Отправляем заявку в чат и на email
        try:
            await send_ticket_to_chat(callback.bot, ticket, ticket_files)
        except Exception as e:
            logger.error(f"Ошибка при отправке в чат: {e}")
        
        try:
            await send_ticket_to_email(ticket, ticket_files)
        except Exception as e:
            logger.error(f"Ошибка при отправке на email: {e}")
        
        # Отправляем подтверждение пользователю
        await callback.message.edit_text(
            f"✅ Заявка успешно создана!\n\n"
            f"Номер заявки: {ticket_number}\n\n"
            f"Ваша заявка отправлена в отдел технической поддержки. "
            f"Мы свяжемся с вами в ближайшее время.\n\n"
            f"Используйте /new для создания новой заявки."
        )
        
        await state.clear()
        await callback.answer("Заявка создана!")
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        logger.error(f"Ошибка при создании заявки: {e}")
        logger.error(f"Детали ошибки:\n{error_details}")
        await callback.message.edit_text(
            f"❌ Произошла ошибка при создании заявки.\n\n"
            f"Ошибка: {str(e)}\n\n"
            f"Пожалуйста, попробуйте еще раз или обратитесь к администратору."
        )
        await callback.answer("Ошибка!")
        await state.clear()


@router.callback_query(StateFilter(TicketForm.confirming), F.data == "confirm_no")
async def cancel_ticket(callback: CallbackQuery, state: FSMContext):
    """Отмена создания заявки"""
    await state.clear()
    await callback.message.edit_text("❌ Создание заявки отменено. Используйте /new для создания новой заявки.")
    await callback.answer()

