from httpx import AsyncClient


async def test_delete_author(ac: AsyncClient, create_authors):
    response = await ac.delete("/authors/1")
    assert response.status_code == 200
    assert response.json()["data"]["last_name"] == "Толстой"

    response = await ac.get("/authors/1")
    assert response.status_code == 404 
