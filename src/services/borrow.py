from datetime import date

from src.exceptions import (
    BookAlreadyReturnedException,
    BookNotFoundException,
    BorrowNotFoundException,
    NoAvailableCopiesException,
    ObjectNotFoundException,
    check_date,
)
from src.schemas.borrow import BorrowAdd
from src.services.base import BaseService


class BorrowService(BaseService):
    async def add_borrow(self, borrow_data: BorrowAdd) -> BorrowAdd:
        try:
            book = await self.db.book.get_by_id(id=borrow_data.book_id)
        except ObjectNotFoundException:
            raise BookNotFoundException

        if book.available_copies <= 0:
            raise NoAvailableCopiesException

        book.available_copies -= 1

        borrow = await self.db.borrow.add(data=borrow_data)
        await self.db.book.edit(id=book.id, data=book)
        await self.db.commit()
        return borrow

    async def get_borrows(self) -> list[BorrowAdd]:
        try:
            return await self.db.borrow.get_all()
        except ObjectNotFoundException:
            raise BorrowNotFoundException

    async def get_borrow_by_id(self, id: int) -> BorrowAdd:
        try:
            return await self.db.borrow.get_by_id(id=id)
        except ObjectNotFoundException:
            raise BorrowNotFoundException

    async def return_borrow(self, id: int, return_date: date) -> BorrowAdd:
        try:
            borrow = await self.db.borrow.get_by_id(id=id)
        except ObjectNotFoundException:
            raise BorrowNotFoundException

        # Если дата возврата раньше даты занятия, то выбрасываем ошибку
        check_date(
            borrow_date=borrow.borrow_date,
            return_date=return_date,
        )

        # Если есть return_date значит займ завершен
        if borrow.return_date:
            raise BookAlreadyReturnedException

        book = await self.db.book.get_by_id(id=borrow.book_id)

        book.available_copies += 1
        borrow.return_date = return_date

        await self.db.book.edit(id=book.id, data=book)
        await self.db.borrow.edit(id=borrow.id, data=borrow)
        await self.db.commit()
        return borrow
