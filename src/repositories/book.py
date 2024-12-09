from src.models.book import BooksORM
from src.repositories.base import BaseRepository


class BookRepository(BaseRepository):
    model = BooksORM
    