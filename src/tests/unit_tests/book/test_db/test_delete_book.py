async def test_delete_book(db):
    deleted_book = await db.book.delete(id=1)
    assert deleted_book.id == 1
    