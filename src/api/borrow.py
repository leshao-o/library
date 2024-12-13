from datetime import date

from fastapi import APIRouter, Body

from src.exceptions import (
    BookAlreadyReturnedException,
    BookAlreadyReturnedHTTPException,
    BookNotFoundException,
    BookNotFoundHTTPException,
    BorrowNotFoundException,
    BorrowNotFoundHTTPException,
    NoAvailableCopiesException,
    NoAvailableCopiesHTTPException,
)
from src.services.borrow import BorrowService
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.borrow import BorrowAdd


router = APIRouter(prefix="/borrows", tags=["Выдачи"])


@router.post(
    "",
    summary="Добавляет новый займ",
    description=(
        """Этот эндпоинт добавляет новый займ в базу данных. 
        Ожидает ID книги, имя читателя и дату займа. 
        Возвращает статус операции и данные нового займа."""
    ),
)
async def add_borrow(
    db: DBDep,
    borrow_data: BorrowAdd = Body(
        openapi_examples={
            "1": {
                "summary": "borrow_1",
                "value": {
                    "book_id": 1,
                    "reader_name": "Андрей",
                    "borrow_date": "2024-12-10",
                },
            },
            "2": {
                "summary": "borrow_2",
                "value": {
                    "book_id": 3,
                    "reader_name": "Алиса",
                    "borrow_date": "2024-12-13",
                },
            },
        }
    ),
):
    try:
        new_borrow = await BorrowService(db).add_borrow(borrow_data=borrow_data)
    except BookNotFoundException:
        raise BookNotFoundHTTPException
    except NoAvailableCopiesException:
        raise NoAvailableCopiesHTTPException

    return {"status": "OK", "data": new_borrow}


@router.get(
    "",
    summary="Возвращает список всех займов",
    description=(
        """Этот эндпоинт возвращает список всех займов из базы данных. 
        Ожидает количество займов на странице и номер страницы. 
        Возвращает статус операции и данные займов для указанной страницы."""
    ),
)
async def get_borrows(db: DBDep, pagin: PaginationDep):
    try:
        borrows = await BorrowService(db).get_borrows()
    except BorrowNotFoundException:
        raise BorrowNotFoundHTTPException

    borrows = borrows[pagin.per_page * (pagin.page - 1):][:pagin.per_page]
    return {"status": "OK", "data": borrows}


@router.get(
    "/{id}",
    summary="Получает займ по ID",
    description=(
        """Этот эндпоинт возвращает информацию о займе по его уникальному идентификатору. 
        Ожидает ID займа. 
        Возвращает статус операции и данные запрашиваемого займа."""
    ),
)
async def get_borrow_by_id(db: DBDep, id: int):
    try:
        borrow = await BorrowService(db).get_borrow_by_id(id=id)
    except BorrowNotFoundException:
        raise BorrowNotFoundHTTPException

    return {"status": "OK", "data": borrow}


@router.patch(
    "/{id}/return",
    summary="Завершает займ книги",
    description=(
        """Этот эндпоинт позволяет отметить займ как возвращённый по его уникальному идентификатору. 
        Ожидает ID займа и дату возврата. 
        Возвращает статус операции и данные о возвращённом займе."""
    ),
)
async def return_borrow(db: DBDep, id: int, return_date: date):
    try:
        returned_borrow = await BorrowService(db).return_borrow(
            id=id, return_date=return_date
        )
    except BorrowNotFoundException:
        raise BorrowNotFoundHTTPException
    except BookAlreadyReturnedException:
        raise BookAlreadyReturnedHTTPException

    return {"status": "OK", "data": returned_borrow}
