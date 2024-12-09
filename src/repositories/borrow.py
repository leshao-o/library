from src.schemas.borrow import Borrow
from src.models.borrow import BorrowsORM
from src.repositories.base import BaseRepository


class BorrowRepository(BaseRepository):
    model = BorrowsORM
    schema = Borrow