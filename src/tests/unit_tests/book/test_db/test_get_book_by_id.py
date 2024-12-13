async def test_get_book_by_id(db):
    book = await db.book.get_by_id(id=1)

    assert book.title == "Война и мир"
    assert book.description == "Эпопея о жизни русского общества в начале 19 века"
    assert book.author_id == 1
    assert book.available_copies == 5
