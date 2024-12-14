import pytest

from src.schemas.author import AuthorPatch


@pytest.mark.parametrize(
    "data, id",
    [
        ({"first_name": "Не Лев"}, 1),
        ({"last_name": "Не Достоевский"}, 2),
        ({"birth_date": "1111-11-11"}, 3),
    ],
)
async def test_edit_author(db, data: dict, id: int):
    data_to_edit = AuthorPatch(**data)
    edited_author = await db.author.edit(id=id, data=data_to_edit)

    # Правую часть приводим к строке, чтобы корректно проверять даты.
    # Это никак не повлияет на другие тесты, тк все другие данные строковые
    assert data[list(data.keys())[0]] == str(
        getattr(edited_author, list(data.keys())[0])
    )
