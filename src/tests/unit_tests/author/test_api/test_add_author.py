from httpx import AsyncClient


async def test_add_author(ac: AsyncClient):
    first_name = "имя"
    last_name = "фамилия"
    birth_date = "2010-10-10"
    id = 6

    response = await ac.post(
        "/authors",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK",
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "id": id,
        },
    }
