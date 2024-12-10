from fastapi import APIRouter, Body

from src.services.book import BookService
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.book import BookAdd, BookPatch


router = APIRouter(prefix="/books", tags=["Книги"])


@router.post("")
async def add_book(
    db: DBDep,
    book_data: BookAdd = Body(
        openapi_examples={
            "1": {
                "summary": "book_1",
                "value": {
                    "title": "Евгений Онегин", 
                    "description": "Первый русский роман в стихах", 
                    "author_id": 2,
                    "available_copies": 5
                },
            },
            "2": {
                "summary": "book_2",
                "value": {
                    "title": "Капитанская дочка", 
                    "description": "", 
                    "author_id": 2,
                    "available_copies": 4
                },
            },
            "3": {
                "summary": "book_3",
                "value": {
                    "title": "Война и мир", 
                    "description": "Очень длинная книга", 
                    "author_id": 5,
                    "available_copies": 8
                },
            }
        }
    )
):
    new_book = await BookService(db).create_book(book_data=book_data)
    return {"status": "OK", "data": new_book}


@router.get("")
async def get_all_books(db: DBDep, pagination: PaginationDep):
    books = await BookService(db).get_all_books()
    books = books[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return {"status": "OK", "data": books}


@router.get("/{id}")
async def get_book_by_id(db: DBDep, id: int):
    book = await BookService(db).get_book_by_id(id=id)
    return {"status": "OK", "data": book}


@router.put("/{id}")
async def edit_book(
    db: DBDep,
    id: int,
    book_data: BookPatch = Body(
        openapi_examples={
            "1": {
                "summary": "book_1",
                "value": {
                    "title": "Евгений Онегин", 
                    "description": "'ЕВГЕНИЙ ОНЕГИН' — первый русский роман в стихах", 
                    "author_id": 2,
                    "available_copies": 5
                },
            },
            "2": {
                "summary": "book_2",
                "value": {
                    "available_copies": 10
                },
            },
            "3": {
                "summary": "book_3",
                "value": {
                    "description": "Очень очень очень длинная книга"
                },
            }
        }
    )
):
    edited_book = await BookService(db).edit_book(id=id, book_data=book_data)
    return {"status": "OK", "data": edited_book}

@router.delete("/{id}")
async def delete_book(db: DBDep, id: int):
    deleted_book = await BookService(db).delete_book(id=id)
    return {"status": "OK", "data": deleted_book}  