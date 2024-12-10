from datetime import date

from fastapi import APIRouter, Body

from src.services.borrow import BorrowService
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.borrow import BorrowAdd


router = APIRouter(prefix="/borrows", tags=["Выдачи"])


@router.post("")
async def add_borrow(
    db: DBDep, 
    borrow_data: BorrowAdd = Body(
        openapi_examples={
            "1": {
                "summary": "borrow_1",
                "value": {
                    "book_id": "1", 
                    "reader_name": "Андрей", 
                    "borrow_date": "2024-12-10"
                },
            },
            "2": {
                "summary": "borrow_2",
                "value": {
                    "book_id": "3", 
                    "reader_name": "Алиса", 
                    "borrow_date": "2024-12-13"
                },
            }
        }
    )
):
    new_borrow = await BorrowService(db).add_borrow(borrow_data=borrow_data)
    return {"status": "OK", "data": new_borrow}


@router.get("")
async def get_all_borrows(db: DBDep, pagination: PaginationDep):
    borrows = await BorrowService(db).get_all_borrows()
    borrows = borrows[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return {"status": "OK", "data": borrows}


@router.get("/{id}")
async def get_borrow_by_id(db: DBDep, id: int):
    borrow = await BorrowService(db).get_borrow_by_id(id=id)
    return {"status": "OK", "data": borrow}


@router.patch("/{id}/return")
async def return_borrow(
    db: DBDep,
    id: int,
    return_date: date
):
    returned_borrow = await BorrowService(db).return_borrow(id=id, return_date=return_date)
    return {"status": "OK", "data": returned_borrow}