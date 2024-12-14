async def test_get_books(db):
    books = await db.book.get_all()
    assert len(books) == 5
