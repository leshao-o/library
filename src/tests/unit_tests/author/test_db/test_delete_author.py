async def test_delete_author(db):
    deleted_author = await db.author.delete(id=1)
    assert deleted_author.id == 1
