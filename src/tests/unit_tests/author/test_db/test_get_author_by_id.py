from datetime import date


async def test_get_author_by_id(db):
    author = await db.author.get_by_id(id=1)

    assert author.first_name == "Лев"
    assert author.last_name == "Толстой"
    assert author.birth_date == date(1828, 9, 9)
