from httpx import AsyncClient


async def test_add_author(ac: AsyncClient, create_authors):
    first_name = "Сергей"
    last_name = "Есенин"
    birth_date = "1895-10-03"
    id = 6

    response = await ac.post("/authors", json={
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date
    })
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK",
        "data": {
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "id": id
        }
    }
