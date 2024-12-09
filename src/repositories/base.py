from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    # добавить данные
    async def add(self, data: BaseModel) -> BaseModel:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()
    
    # получить все данные
    async def get_all(self) -> list[BaseModel]:
        query = select(self.model)
        result = await self.session.execute(query)
        return [one for one in result.scalars().all()]

    # получить данные по id
    async def get_by_id(self, id: int) -> BaseModel:
        query = select(self.model).filter(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalars().one()

    # изменить только те данные которые были переданы
    async def edit(self, data: BaseModel, **filter_by) -> BaseModel:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one()
    
    # удалить данные по нужным фильтрам
    async def delete(self, **filter_by) -> BaseModel:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one()
