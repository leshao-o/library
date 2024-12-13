import pytest
from httpx import ASGITransport, AsyncClient

from src.schemas.book import BookAdd
from src.api.dependencies import get_db
from src.schemas.author import AuthorAdd
from src.models import *
from src.config import settings
from src.main import app
from src.utils.setup_test_db import get_data_from_json, setup_database
from src.utils.db_manager import DBManager
from src.database import async_session_maker


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


# создаем таблицы, добавляем авторов, удаляем таблицы после теста
@pytest.fixture(scope="module", autouse=True)
async def create_test_data(check_test_mode):
    authors_data = get_data_from_json("src/tests/mock_authors.json")
    authors = [AuthorAdd.model_validate(author) for author in authors_data]
    books_data = get_data_from_json("src/tests/mock_books.json")
    books = [BookAdd.model_validate(book) for book in books_data]

    await setup_database()

    async with DBManager(session_factory=async_session_maker) as db_:
        await db_.author.add_bulk(authors)
        await db_.book.add_bulk(books)
        await db_.commit()

    yield

    await setup_database()


# Фикстура для получения асинхронного соединения с базой данных
@pytest.fixture()
async def db():
    async for db in get_db():
        yield db


# Фикстура для создания асинхронного клиента HTTP, 
# который будет использоваться для выполнения запросов к API
@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
