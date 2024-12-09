from datetime import date

from pydantic import BaseModel


class AuthorAdd(BaseModel):
    first_name: str
    last_name: str
    birth_date: date


# модель для частичного изменения данных
class AuthorPatch(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None


class Author(AuthorAdd):
    id: int