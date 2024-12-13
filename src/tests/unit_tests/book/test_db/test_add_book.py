from src.schemas.book import BookAdd


async def test_add_book(db):
    book = BookAdd(
        title="test_book",
        description="test_desc",
        author_id=1,
        available_copies=100
    )

    new_book = await db.book.add(data=book)
    await db.commit()

    assert new_book.title == book.title
    assert new_book.description == book.description
    assert new_book.author_id == book.author_id
    assert new_book.available_copies == book.available_copies
    