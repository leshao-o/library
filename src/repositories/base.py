from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    # добавить данные
    async def add(self, data: BaseModel) -> BaseModel:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return self.schema.model_validate(result.scalars().one(), from_attributes=True)
    
    # получить все данные
    async def get_all(self) -> list[BaseModel]:
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(one, from_attributes=True) for one in result.scalars().all()]

    # получить данные по id
    async def get_by_id(self, id: int) -> BaseModel:
        query = select(self.model).filter(self.model.id == id)
        result = await self.session.execute(query)
        return self.schema.model_validate(result.scalars().one(), from_attributes=True)

    # изменить только те данные которые были переданы
    async def edit(self, data: BaseModel, **filter_by) -> BaseModel:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return self.schema.model_validate(result.scalars().one(), from_attributes=True)
    
    # удалить данные по нужным фильтрам
    async def delete(self, **filter_by) -> BaseModel:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        return self.schema.model_validate(result.scalars().one(), from_attributes=True)
