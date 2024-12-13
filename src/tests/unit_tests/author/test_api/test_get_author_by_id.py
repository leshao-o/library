from httpx import AsyncClient


async def test_get_author_by_id(ac: AsyncClient):
    response = await ac.get("/authors/2")
    assert response.status_code == 200
    assert response.json()["data"]["last_name"] == "Достоевский"
    