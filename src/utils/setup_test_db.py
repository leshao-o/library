import json

from src.database import Base, engine


async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def get_data_from_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.loads(file.read())
    return data
