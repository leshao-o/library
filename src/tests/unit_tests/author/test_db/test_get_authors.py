async def test_get_authors(db):
    authors = await db.author.get_all()
    assert len(authors) == 5
    