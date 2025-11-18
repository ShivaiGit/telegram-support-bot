"""Модели базы данных"""
from datetime import datetime
from typing import Optional, List
import aiosqlite


class Ticket:
    """Модель заявки"""
    
    def __init__(
        self,
        ticket_number: str,
        user_id: int,
        phone: str,
        description: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        priority: str = "medium",
        status: str = "new",
        ticket_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = ticket_id
        self.ticket_number = ticket_number
        self.user_id = user_id
        self.username = username
        self.phone = phone
        self.email = email
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    async def create(cls, ticket_number: str, user_id: int, phone: str, 
                    description: str, username: Optional[str] = None,
                    email: Optional[str] = None, priority: str = "medium") -> 'Ticket':
        """Создание новой заявки"""
        async with aiosqlite.connect("tickets.db") as db:
            cursor = await db.execute("""
                INSERT INTO tickets 
                (ticket_number, user_id, username, phone, email, description, priority, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'new')
            """, (ticket_number, user_id, username, phone, email, description, priority))
            await db.commit()
            ticket_id = cursor.lastrowid
            
            # Получаем созданную заявку
            async with db.execute("""
                SELECT * FROM tickets WHERE id = ?
            """, (ticket_id,)) as cursor:
                row = await cursor.fetchone()
                return cls._from_row(row)
    
    @classmethod
    def _from_row(cls, row):
        """Создание объекта из строки БД"""
        if not row:
            return None
        return cls(
            ticket_id=row[0],
            ticket_number=row[1],
            user_id=row[2],
            username=row[3],
            phone=row[4],
            email=row[5],
            description=row[6],
            priority=row[7],
            status=row[8],
            created_at=datetime.fromisoformat(row[9]) if row[9] else None,
            updated_at=datetime.fromisoformat(row[10]) if row[10] else None
        )
    
    @classmethod
    async def get_by_number(cls, ticket_number: str) -> Optional['Ticket']:
        """Получение заявки по номеру"""
        async with aiosqlite.connect("tickets.db") as db:
            async with db.execute("""
                SELECT * FROM tickets WHERE ticket_number = ?
            """, (ticket_number,)) as cursor:
                row = await cursor.fetchone()
                return cls._from_row(row) if row else None
    
    @classmethod
    async def get_by_user_id(cls, user_id: int, limit: int = 10) -> List['Ticket']:
        """Получение заявок пользователя"""
        async with aiosqlite.connect("tickets.db") as db:
            async with db.execute("""
                SELECT * FROM tickets WHERE user_id = ? 
                ORDER BY created_at DESC LIMIT ?
            """, (user_id, limit)) as cursor:
                rows = await cursor.fetchall()
                return [cls._from_row(row) for row in rows]
    
    @classmethod
    async def get_next_ticket_number(cls) -> str:
        """Генерация следующего номера заявки"""
        async with aiosqlite.connect("tickets.db") as db:
            async with db.execute("""
                SELECT COUNT(*) FROM tickets
            """) as cursor:
                count = (await cursor.fetchone())[0]
                return f"TICKET-{count + 1:04d}"


class TicketFile:
    """Модель файла заявки"""
    
    def __init__(self, ticket_id: int, file_id: str, file_type: Optional[str] = None,
                 file_path: Optional[str] = None, file_id_db: Optional[int] = None):
        self.id = file_id_db
        self.ticket_id = ticket_id
        self.file_id = file_id
        self.file_type = file_type
        self.file_path = file_path
    
    @classmethod
    async def create(cls, ticket_id: int, file_id: str, 
                    file_type: Optional[str] = None,
                    file_path: Optional[str] = None) -> 'TicketFile':
        """Создание записи о файле"""
        async with aiosqlite.connect("tickets.db") as db:
            await db.execute("""
                INSERT INTO ticket_files (ticket_id, file_id, file_type, file_path)
                VALUES (?, ?, ?, ?)
            """, (ticket_id, file_id, file_type, file_path))
            await db.commit()
            return cls(ticket_id, file_id, file_type, file_path)
    
    @classmethod
    async def get_by_ticket_id(cls, ticket_id: int) -> List['TicketFile']:
        """Получение файлов заявки"""
        async with aiosqlite.connect("tickets.db") as db:
            async with db.execute("""
                SELECT * FROM ticket_files WHERE ticket_id = ?
            """, (ticket_id,)) as cursor:
                rows = await cursor.fetchall()
                return [
                    cls(
                        file_id_db=row[0],
                        ticket_id=row[1],
                        file_id=row[2],
                        file_type=row[3],
                        file_path=row[4]
                    )
                    for row in rows
                ]

