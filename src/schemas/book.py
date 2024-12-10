from pydantic import BaseModel


class BookAdd(BaseModel):
    title: str
    description: str | None = None
    author_id: int
    available_copies: int


# Модель для частичного изменения данных
class BookPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    author_id: int | None = None
    available_copies: int | None = None


class Book(BookAdd):
    id: int