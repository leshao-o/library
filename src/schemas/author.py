from datetime import date

from pydantic import BaseModel


class AuthorAdd(BaseModel):
    first_name: str
    last_name: str
    birth_date: date


class Author(AuthorAdd):
    id: int