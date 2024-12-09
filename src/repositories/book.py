from src.schemas.book import Book
from src.models.book import BooksORM
from src.repositories.base import BaseRepository


class BookRepository(BaseRepository):
    model = BooksORM
    schema = Book