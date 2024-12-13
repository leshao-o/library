from src.schemas.borrow import BorrowAdd


async def test_add_borrow(db):
    borrow = BorrowAdd(
        book_id = "1",
        reader_name = "имя читателя",
        borrow_date = "2010-10-10",
    )
    
    new_borrow = await db.borrow.add(data=borrow)
    await db.commit()

    assert new_borrow.book_id == borrow.book_id
    assert new_borrow.reader_name == borrow.reader_name
    assert new_borrow.borrow_date == borrow.borrow_date
