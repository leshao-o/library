from src.repositories.borrow import BorrowRepository
from src.repositories.book import BookRepository
from src.repositories.author import AuthorRepository 


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = BorrowRepository(self.session)
        self.hotels = BookRepository(self.session)
        self.hotels = AuthorRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
