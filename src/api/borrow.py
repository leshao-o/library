from fastapi import APIRouter, Body

from src.services.borrow import BorrowService
from src.api.dependencies import DBDep
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
                    "borrow_date": "2024-12-10",
                    "return_date": "2024-12-20"
                },
            },
            "2": {
                "summary": "borrow_2",
                "value": {
                    "book_id": "3", 
                    "reader_name": "Алиса", 
                    "borrow_date": "2024-12-13",
                    "return_date": "2024-12-29"
                },
            }
        }
    )
):
    new_borrow = await BorrowService(db).add_borrow(borrow_data=borrow_data)
    return {"status": "OK", "data": new_borrow}

@router.get("")
async def get_all_borrows(db: DBDep):
    borrows = await BorrowService(db).get_all_borrows()
    return {"status": "OK", "data": borrows}
