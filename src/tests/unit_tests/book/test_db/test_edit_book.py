import pytest

from src.schemas.book import BookPatch


@pytest.mark.parametrize(
    "data, id", 
    [
        ({"title": "Мир и война"}, 1),
        ({"description": "Роман о преступлении и наказании"}, 2),
        ({"author_id": 4}, 3),
        ({"available_copies": 100}, 4)
    ]
)
async def test_edit_book(db, data: dict, id: int):
    data_to_edit = BookPatch(**data)
    edited_book = await db.book.edit(id=id, data=data_to_edit)

    assert data[list(data.keys())[0]] == getattr(edited_book, list(data.keys())[0])
