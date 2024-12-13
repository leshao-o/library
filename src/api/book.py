from fastapi import APIRouter, Body

from src.exceptions import (
    BookNotFoundException,
    BookNotFoundHTTPException,
    InvalidInputException,
    InvalidInputHTTPException,
)
from src.services.book import BookService
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.book import BookAdd, BookPatch


router = APIRouter(prefix="/books", tags=["Книги"])


@router.post(
    "",
    summary="Добавляет новую книгу",
    description=(
        """Этот эндпоинт добавяет новую книгу в базу данных. 
        Ожидает данные о книге, включая название, описание, ID автора и количество доступных копий. 
        Возвращает статус операции и данные добавленной книги."""
    ),
)
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
                    "available_copies": 5,
                },
            },
            "2": {
                "summary": "book_2",
                "value": {
                    "title": "Капитанская дочка",
                    "description": "",
                    "author_id": 2,
                    "available_copies": 4,
                },
            },
            "3": {
                "summary": "book_3",
                "value": {
                    "title": "Война и мир",
                    "description": "Очень длинная книга",
                    "author_id": 5,
                    "available_copies": 8,
                },
            },
        }
    ),
):
    new_book = await BookService(db).create_book(book_data=book_data)
    return {"status": "OK", "data": new_book}


@router.get(
    "",
    summary="Получает список всех книг",
    description=(
        """Этот эндпоинт возвращает список всех книг из базы данных. 
        Ожидает количество книг на странице и номер страницы. 
        Возвращает статус операции и данные книг для указанной страницы."""
    ),
)
async def get_books(db: DBDep, pagination: PaginationDep):
    try:
        books = await BookService(db).get_books()
    except BookNotFoundException:
        raise BookNotFoundHTTPException

    books = books[pagination.per_page * (pagination.page - 1) :][: pagination.per_page]
    return {"status": "OK", "data": books}


@router.get(
    "/{id}",
    summary="Возвращает книгу по ID",
    description=(
        """Этот эндпоинт возвращает информацию о книге по её уникальному идентификатору. 
        Ожидает ID книги. 
        Возвращает статус операции и данные запрашиваемой книги."""
    ),
)
async def get_book_by_id(db: DBDep, id: int):
    try:
        book = await BookService(db).get_book_by_id(id=id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException

    return {"status": "OK", "data": book}


@router.put(
    "/{id}",
    summary="Редактирует книгу",
    description=(
        """Этот эндпоинт редактирует информацию о книге по её уникальному идентификатору. 
        Ожидает ID книги и необязательные данные для обновления: название, описание, ID автора и количество доступных копий. 
        Возвращает статус операции и обновленные данные книги."""
    ),
)
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
                    "available_copies": 5,
                },
            },
            "2": {
                "summary": "book_2",
                "value": {"available_copies": 10},
            },
            "3": {
                "summary": "book_3",
                "value": {"description": "Очень очень очень длинная книга"},
            },
        }
    ),
):
    try:
        edited_book = await BookService(db).edit_book(id=id, book_data=book_data)
    except InvalidInputException:
        raise InvalidInputHTTPException
    except BookNotFoundException:
        raise BookNotFoundHTTPException

    return {"status": "OK", "data": edited_book}


@router.delete(
    "/{id}",
    summary="Удаляет книгу",
    description=(
        """Этот эндпоинт удаляет книгу из базы данных по её уникальному идентификатору. 
        Ожидает ID книги. 
        Возвращает статус операции и данные удалённой книги."""
    ),
)
async def delete_book(db: DBDep, id: int):
    try:
        deleted_book = await BookService(db).delete_book(id=id)
    except BookNotFoundException:
        raise BookNotFoundHTTPException

    return {"status": "OK", "data": deleted_book}
