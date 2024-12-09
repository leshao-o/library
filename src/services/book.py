from src.schemas.book import BookAdd
from src.services.base import BaseService


class BookService(BaseService):
    async def create_book(self, book_data: BookAdd) -> BookAdd:
        book = await self.db.book.add(data=book_data)
        await self.db.commit()
        return book
    
    async def get_all_books(self) -> list[BookAdd]:
        return await self.db.book.get_all()
    
    async def get_book_by_id(self, id: int) -> BookAdd:
        return await self.db.book.get_by_id(id=id)
    