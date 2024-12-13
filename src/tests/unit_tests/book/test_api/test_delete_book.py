from httpx import AsyncClient


async def test_delete_book(ac: AsyncClient):
    response = await ac.delete("/books/1")
    assert response.status_code == 200
    assert response.json()["data"]["title"] == "Война и мир"

    response = await ac.get("/books/1")
    assert response.status_code == 404 
