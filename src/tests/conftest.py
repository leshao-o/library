import pytest
from typing import AsyncGenerator
from pydantic import BaseModel
from httpx import ASGITransport, AsyncClient
from unittest import mock

# Мокаем декоратор кэширования для тестирования этих ручек
mock.patch("fastapi_cache.decorator.cache", lambda *args, **krwargs: lambda f: f).start()

from src.schemas.borrow import BorrowAdd
from src.schemas.book import BookAdd
from src.schemas.author import AuthorAdd
from src.api.dependencies import get_db
from src.models import *  # noqa
from src.config import settings
from src.main import app
from src.utils.setup_test_db import get_data_from_json, setup_database
from src.utils.db_manager import DBManager
from src.database import async_session_maker


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


# Создаем таблицы, добавляем данные, удаляем таблицы после теста
@pytest.fixture(scope="module", autouse=True)
async def create_test_data(check_test_mode):
    # Функция для загрузки и валидации данных из JSON
    async def load_and_validate_data(file_path: str, schema: BaseModel):
        data = get_data_from_json(file_path)
        return [schema.model_validate(item) for item in data]
    
    authors = await load_and_validate_data("src/tests/data/mock_authors.json", AuthorAdd)
    books = await load_and_validate_data("src/tests/data/mock_books.json", BookAdd)
    borrows = await load_and_validate_data("src/tests/data/mock_borrows.json", BorrowAdd)

    await setup_database()

    async with DBManager(session_factory=async_session_maker) as db_:
        await db_.author.add_bulk(authors)
        await db_.book.add_bulk(books)
        await db_.borrow.add_bulk(borrows)
        await db_.commit()


# Фикстура для получения асинхронного соединения с базой данных
@pytest.fixture()
async def db() -> AsyncGenerator[DBManager, None]:
    async for db in get_db():
        yield db


# Фикстура для создания асинхронного клиента HTTP,
# который будет использоваться для выполнения запросов к API
@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
