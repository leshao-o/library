from datetime import date

from pydantic import BaseModel


class BorrowAdd(BaseModel):
    book_id: int
    reader_name: str
    borrow_date: date
    return_date: date | None = None


class Borrow(BorrowAdd):
    id: int