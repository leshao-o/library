from src.schemas.book import BookAdd
from src.services.base import BaseService


class BookService(BaseService):
    async def create_book(self, book_data: BookAdd) -> BookAdd:
        book = await self.db.book.add(book_data)
        await self.db.commit()
        return book
    
    