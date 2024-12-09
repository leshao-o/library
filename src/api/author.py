from fastapi import APIRouter, Body

from src.services.author import AuthorService
from src.api.dependencies import DBDep
from src.schemas.author import AuthorAdd, AuthorPatch

router = APIRouter(prefix="/authors", tags=["Автор"])


@router.post("")
async def add_author(
    db: DBDep, 
    author_data: AuthorAdd = Body(
        openapi_examples={
            "1": {
                "summary": "author_1",
                "value": {
                    "first_name": "Александр", 
                    "last_name": "Пушкин", 
                    "birth_date": "1799-06-06"
                },
            },
            "2": {
                "summary": "author_2",
                "value": {
                    "first_name": "Лев", 
                    "last_name": "Толстой", 
                    "birth_date": "1828-09-09"
                },
            }
        }
    ),
):
    author = await AuthorService(db).create_author(author_data=author_data)
    return {"status": "OK", "data": author}


@router.get("")
async def get_all_authors(db: DBDep):
    authors = await AuthorService(db).get_all_authors()
    return {"status": "OK", "data": authors}


@router.get("/{id}")
async def get_author_by_id(db: DBDep, id: int):
    author = await AuthorService(db).get_author_by_id(id=id)
    return {"status": "OK", "data": author}


@router.put("/{id}")
async def edit_author_data(
    db: DBDep, 
    id: int,
    author_data: AuthorPatch = Body(
        openapi_examples={
            "1": {
                "summary": "author_1",
                "value": { 
                    "last_name": "Грибоедов", 
                    "birth_date": "1795-01-15"
                },
            },
            "2": {
                "summary": "author_2",
                "value": {
                    "first_name": "Михаил", 
                    "last_name": "Ломоносов", 
                    "birth_date": "1711-11-19"
                },
            }
        }
    ),
):
    author = await AuthorService(db).edit_author_data(id=id, author_data=author_data)
    return {"status": "OK", "data": author}


@router.delete("/{id}")
async def delete_author(db: DBDep, id: int):
    author = await AuthorService(db).delete_author(id=id)
    return {"status": "OK", "data": author}
