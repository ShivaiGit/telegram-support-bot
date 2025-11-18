"""Состояния FSM для диалога с пользователем"""
from aiogram.fsm.state import State, StatesGroup


class TicketForm(StatesGroup):
    """Состояния формы создания заявки"""
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_location = State()
    waiting_for_description = State()
    waiting_for_priority = State()
    waiting_for_files = State()
    confirming = State()

