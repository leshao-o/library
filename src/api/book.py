from fastapi import APIRouter, Body

from src.services.book import BookService
from src.api.dependencies import DBDep
from src.schemas.book import BookAdd

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
                    "author_id": "2",
                    "available_copies": 5
                },
            },
            "2": {
                "summary": "book_2",
                "value": {
                    "title": "Капитанская дочка", 
                    "description": "", 
                    "author_id": "2",
                    "available_copies": 4
                },
            },
            "3": {
                "summary": "book_3",
                "value": {
                    "title": "Война и мир", 
                    "description": "Очень длинная книга", 
                    "author_id": "5",
                    "available_copies": 8
                },
            }
        }
    ),
):
    book = await BookService(db).create_book(book_data=book_data)
    return {"status": "OK", "data": book}

