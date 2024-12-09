from src.schemas.book import BookAdd
from src.services.base import BaseService


class BookService(BaseService):
    async def create_book(self, book_data: BookAdd) -> BookAdd:
        new_book = await self.db.book.add(data=book_data)
        await self.db.commit()
        return new_book
    
    async def get_all_books(self) -> list[BookAdd]:
        return await self.db.book.get_all()
    
    async def get_book_by_id(self, id: int) -> BookAdd:
        return await self.db.book.get_by_id(id=id)
    
    async def edit_book(self, id: int, book_data: BookAdd) -> BookAdd:
        edited_book = await self.db.book.edit(id=id, data=book_data)
        await self.db.commit()
        return edited_book
    
    async def delete_book(self, id: int) -> BookAdd:
        deleted_book = await self.db.book.delete(id=id)
        await self.db.commit()
        return deleted_book