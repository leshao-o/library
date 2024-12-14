from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "data, id",
    [
        ({"first_name": "Не Лев"}, 1),
        ({"last_name": "Не Достоевский"}, 2),
        ({"birth_date": "1111-11-11"}, 3),
    ],
)
async def test_edit_author(ac: AsyncClient, data: dict, id: int):
    response = await ac.put(f"/authors/{id}", json=data)

    assert response.status_code == 200
    # Проверяем из полученного ответа, что данные которые передали изменились
    assert response.json()["data"][list(data.keys())[0]] == list(data.values())[0]
