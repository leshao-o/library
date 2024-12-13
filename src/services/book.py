from src.exceptions import (
    BookNotFoundException,
    InvalidInputException,
    ObjectNotFoundException,
)
from src.schemas.book import BookAdd
from src.services.base import BaseService


class BookService(BaseService):
    async def create_book(self, book_data: BookAdd) -> BookAdd:
        new_book = await self.db.book.add(data=book_data)
        await self.db.commit()
        return new_book

    async def get_books(self) -> list[BookAdd]:
        try:
            return await self.db.book.get_all()
        except ObjectNotFoundException:
            raise BookNotFoundException

    async def get_book_by_id(self, id: int) -> BookAdd:
        try:
            return await self.db.book.get_by_id(id=id)
        except ObjectNotFoundException:
            raise BookNotFoundException

    async def edit_book(self, id: int, book_data: BookAdd) -> BookAdd:
        try:
            edited_book = await self.db.book.edit(id=id, data=book_data)
        except InvalidInputException:
            raise InvalidInputException
        except ObjectNotFoundException:
            raise BookNotFoundException

        await self.db.commit()
        return edited_book

    async def delete_book(self, id: int) -> BookAdd:
        try:
            deleted_book = await self.db.book.delete(id=id)
        except ObjectNotFoundException:
            raise BookNotFoundException

        await self.db.commit()
        return deleted_book
