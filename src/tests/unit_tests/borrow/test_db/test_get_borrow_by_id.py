async def test_get_borrow_by_id(db):
    borrow = await db.borrow.get_by_id(id=1)
    assert borrow.id == 1
    assert borrow.book_id == 1
    assert borrow.reader_name == "Андрей"
    assert str(borrow.borrow_date) == "2024-12-10"

