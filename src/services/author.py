from src.exceptions import (
    AuthorNotFoundException,
    InvalidInputException,
    ObjectNotFoundException,
)
from src.schemas.author import AuthorAdd, AuthorPatch
from src.services.base import BaseService


class AuthorService(BaseService):
    async def create_author(self, author_data: AuthorAdd) -> AuthorAdd:
        new_author = await self.db.author.add(data=author_data)
        await self.db.commit()
        return new_author

    async def get_all_authors(self) -> list[AuthorAdd]:
        try:
            return await self.db.author.get_all()
        except ObjectNotFoundException:
            raise AuthorNotFoundException

    async def get_author_by_id(self, id: int) -> AuthorAdd:
        try:
            return await self.db.author.get_by_id(id=id)
        except ObjectNotFoundException:
            raise AuthorNotFoundException

    async def edit_author(self, id: int, author_data: AuthorPatch) -> AuthorAdd:
        try:
            edited_author = await self.db.author.edit(id=id, data=author_data)
        except InvalidInputException:
            raise InvalidInputException
        except ObjectNotFoundException:
            raise AuthorNotFoundException

        await self.db.commit()
        return edited_author

    async def delete_author(self, id: int) -> AuthorAdd:
        try:
            deleted_author = await self.db.author.delete(id=id)
        except ObjectNotFoundException:
            raise AuthorNotFoundException

        await self.db.commit()
        return deleted_author
