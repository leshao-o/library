from src.schemas.author import Author
from src.models.author import AuthorsORM
from src.repositories.base import BaseRepository


class AuthorRepository(BaseRepository):
    model = AuthorsORM
    schema = Author