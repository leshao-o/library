from httpx import AsyncClient


async def test_get_book_by_id(ac: AsyncClient):
    response = await ac.get("/books/2")
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Преступление и наказание"
