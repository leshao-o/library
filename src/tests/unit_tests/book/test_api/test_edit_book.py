from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "data, id", 
    [
        ({"title": "Мир и война"}, 1),
        ({"description": "Роман о преступлении и наказании"}, 2),
        ({"author_id": 4}, 3),
        ({"available_copies": 100}, 4)
    ]
)
async def test_edit_book(ac: AsyncClient, data: dict, id: int):
    response = await ac.put(f"/books/{id}", json=data)

    assert response.status_code == 200
    # Проверяем из полученного ответа, что данные которые передали изменились
    assert response.json()["data"][list(data.keys())[0]] == list(data.values())[0]
    