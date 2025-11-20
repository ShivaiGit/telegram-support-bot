"""Инициализация и управление базой данных"""
import aiosqlite
from config import Config


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect("tickets.db") as db:
        # Создание таблицы tickets
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_number VARCHAR(50) UNIQUE NOT NULL,
                user_id BIGINT NOT NULL,
                username VARCHAR(255),
                phone VARCHAR(50) NOT NULL,
                email VARCHAR(255),
                location VARCHAR(500),
                description TEXT NOT NULL,
                priority VARCHAR(20) DEFAULT 'medium',
                status VARCHAR(20) DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Добавляем колонку location, если её нет (для существующих БД)
        # Проверяем существование колонки через PRAGMA
        try:
            async with db.execute("PRAGMA table_info(tickets)") as cursor:
                columns = await cursor.fetchall()
                column_names = [col[1] for col in columns]
                if 'location' not in column_names:
                    await db.execute("ALTER TABLE tickets ADD COLUMN location VARCHAR(500)")
                    await db.commit()
        except Exception:
            # Если не удалось проверить, пробуем добавить
            try:
                await db.execute("ALTER TABLE tickets ADD COLUMN location VARCHAR(500)")
                await db.commit()
            except aiosqlite.OperationalError:
                # Колонка уже существует
                pass
        
        # Создание таблицы ticket_files
        await db.execute("""
            CREATE TABLE IF NOT EXISTS ticket_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                file_id VARCHAR(255) NOT NULL,
                file_type VARCHAR(50),
                file_path VARCHAR(500),
                FOREIGN KEY (ticket_id) REFERENCES tickets(id)
            )
        """)
        
        # Создание индексов
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_ticket_number ON tickets(ticket_number)
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_id ON tickets(user_id)
        """)
        await db.execute("""
            CREATE INDEX IF NOT EXISTS idx_ticket_files_ticket_id ON ticket_files(ticket_id)
        """)
        
        await db.commit()


async def get_db():
    """Получение соединения с БД"""
    return await aiosqlite.connect("tickets.db")

