from src.schemas.borrow import BorrowAdd
from src.services.base import BaseService


class BorrowService(BaseService):
    async def add_borrow(self, borrow_data: BorrowAdd) -> BorrowAdd:
        borrow = await self.db.borrow.add(data=borrow_data)
        await self.db.commit()
        return borrow

    async def get_all_borrows(self) -> list[BorrowAdd]:
        return await self.db.borrow.get_all()
    