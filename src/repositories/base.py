from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, ProgrammingError

from src.exceptions import InvalidInputException, ObjectNotFoundException


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    # Добавить данные
    async def add(self, data: BaseModel) -> BaseModel:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model

    # Получить все данные
    async def get_all(self) -> list[BaseModel]:
        query = select(self.model)
        result = await self.session.execute(query)
        try:
            models = [
                self.schema.model_validate(one, from_attributes=True)
                for one in result.scalars().all()
            ]
        except NoResultFound:
            raise ObjectNotFoundException

        return models

    # Получить данные по id
    async def get_by_id(self, id: int) -> BaseModel:
        query = select(self.model).filter(self.model.id == id)
        result = await self.session.execute(query)
        try:
            model = self.schema.model_validate(
                result.scalars().one(), from_attributes=True
            )
        except NoResultFound:
            raise ObjectNotFoundException

        return model

    # Изменить только те данные которые были переданы
    async def edit(self, data: BaseModel, **filter_by) -> BaseModel:
        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        try:
            result = await self.session.execute(stmt)
            model = self.schema.model_validate(
                result.scalars().one(), from_attributes=True
            )
        except ProgrammingError:
            raise InvalidInputException
        except NoResultFound:
            raise ObjectNotFoundException

        return model

    # Удалить данные по нужным фильтрам
    async def delete(self, **filter_by) -> BaseModel:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            model = self.schema.model_validate(
                result.scalars().one(), from_attributes=True
            )
        except NoResultFound:
            raise ObjectNotFoundException

        return model
