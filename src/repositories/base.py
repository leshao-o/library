from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import NoResultFound, ProgrammingError, IntegrityError

from src.exceptions import InvalidInputException, ObjectNotFoundException


class BaseRepository:
    # Определяем модель и схему, которые будут использоваться в репозитории
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    # Метод для добавления данных в базу
    async def add(self, data: BaseModel) -> BaseModel:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(stmt)
        except IntegrityError:
            raise ObjectNotFoundException
        # Валидация (приведение результата к pydantic модели) и возврат добавленной модели
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model

    # Метод для добавления сразу нескольких данных
    async def add_bulk(self, data: list[BaseModel]) -> None:
        stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(stmt)

    # Метод для получения всех данных из таблицы
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

    # Метод для получения данных по ID
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

    # Метод для изменения данных, которые передали
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

    # Метод для удаления данных по заданным фильтрам
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
