from pydantic import BaseModel


class BookAdd(BaseModel):
    title: str
    description: str | None = None
    author_id: int
    available_copies: int


class Book(BookAdd):
    id: int