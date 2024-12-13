async def test_get_borrows(db):
    borrows = await db.borrow.get_all()
    assert len(borrows) == 5
    