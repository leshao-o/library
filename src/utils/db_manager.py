from src.repositories.borrow import BorrowRepository
from src.repositories.book import BookRepository
from src.repositories.author import AuthorRepository


class DBManager:
    """
    Асинхронный контекстный менеджер для управления сессиями базы данных. 
    Создает новую сессию с БД и инициализирует репозитории для работы с ними
    """
    
    def __init__(self, session_factory):
        self.session_factory = session_factory

    # Создается новая сессия и инициализируются репозитории, 
    # которые будут использовать эту сессию
    async def __aenter__(self):
        self.session = self.session_factory()

        self.borrow = BorrowRepository(self.session)
        self.book = BookRepository(self.session)
        self.author = AuthorRepository(self.session)

        return self

    # Происходит откат изменений и закрытие сессии, что помогает избежать 
    # утечек ресурсов и гарантирует, что сессия будет корректно завершена
    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    # Метод для фиксации изменений в базе данных
    async def commit(self):
        await self.session.commit()
