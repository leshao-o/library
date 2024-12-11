import pytest
from httpx import AsyncClient

from src.database import Base, engine_null_pool
from src.models import *
from src.config import settings
from src.main import app


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    print(settings.DB_NAME)
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# Создание асинхронного клиента для выполнения запросов к API
@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
