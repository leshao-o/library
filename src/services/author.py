from src.schemas.author import AuthorAdd, AuthorPatch
from src.services.base import BaseService


class AuthorService(BaseService):
    async def create_author(self, author_data: AuthorAdd) -> AuthorAdd:
        author = await self.db.author.add(author_data)
        await self.db.commit()
        return author
    
    async def get_all_authors(self) -> list[AuthorAdd]:
        return await self.db.author.get_all()
        
    async def get_author_by_id(self, id: int) -> AuthorAdd:
        return await self.db.author.get_by_id(id=id)
    
    async def edit_author_data(self, id: int, author_data: AuthorPatch) -> AuthorAdd:
        author = await self.db.author.edit(id=id, data=author_data)
        await self.db.commit()
        return author
    
    async def delete_author(self, id: int) -> AuthorAdd:
        author = await self.db.author.delete(id=id)
        await self.db.commit()
        return author