from datetime import date

from src.schemas.borrow import BorrowAdd
from src.services.base import BaseService


class BorrowService(BaseService):
    async def add_borrow(self, borrow_data: BorrowAdd) -> BorrowAdd:
        book = await self.db.book.get_by_id(id=borrow_data.book_id)
        if book.available_copies <= 0:
            raise Exception("Нет доступных экземпляров книги для выдачи.")
        
        book.available_copies -= 1

        borrow = await self.db.borrow.add(data=borrow_data)
        await self.db.book.edit(id=book.id, data=book)
        await self.db.commit()
        return borrow

    async def get_all_borrows(self) -> list[BorrowAdd]:
        return await self.db.borrow.get_all()
    
    async def get_borrow_by_id(self, id: int) -> BorrowAdd:
        return await self.db.borrow.get_by_id(id=id)
    
    async def return_borrow(self, id: int, return_date: date) -> BorrowAdd:
        borrow = await self.db.borrow.get_by_id(id=id)
        # Если есть return_date значит займ завершен
        if borrow.return_date:
            raise Exception("Книга уже была возвращена по этому займу")
        book = await self.db.book.get_by_id(id=borrow.book_id)

        book.available_copies += 1
        borrow.return_date = return_date
        
        await self.db.book.edit(id=book.id, data=book)
        await self.db.borrow.edit(id=borrow.id, data=borrow)
        await self.db.commit()
        return borrow