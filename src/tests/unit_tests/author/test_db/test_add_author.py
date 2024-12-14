from src.schemas.author import AuthorAdd


async def test_add_author(db):
    author = AuthorAdd(
        first_name="Сергей",
        last_name="Есенин",
        birth_date="1895-10-03",
    )

    new_author = await db.author.add(author)
    await db.commit()

    assert new_author.first_name == author.first_name
    assert new_author.last_name == author.last_name
    assert new_author.birth_date == author.birth_date
