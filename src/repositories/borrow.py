from src.models.borrow import BorrowsORM
from src.repositories.base import BaseRepository


class BorrowRepository(BaseRepository):
    model = BorrowsORM
    