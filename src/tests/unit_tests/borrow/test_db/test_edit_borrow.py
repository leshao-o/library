import pytest

from schemas.borrow import BorrowPatch


@pytest.mark.parametrize(
    "data, id",
    [
        ({"book_id": 2}, 1),
        ({"reader_name": "Роман"}, 2),
        ({"borrow_date": "2024-11-11"}, 3),
        ({"return_date": "2024-12-15"}, 4),
    ],
)
async def test_edit_borrow(db, data, id):
    borrow = BorrowPatch(**data)
    edited_borrow = await db.borrow.edit(id=id, data=borrow)

    assert str(data[list(data.keys())[0]]) == str(
        getattr(edited_borrow, list(data.keys())[0])
    )
