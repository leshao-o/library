async def test_get_author_by_id(db):
    author = await db.author.get_by_id(id=1)

    assert author.first_name == "Лев"
    assert author.last_name == "Толстой"
    assert str(author.birth_date) == "1828-09-09"
