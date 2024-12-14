from httpx import AsyncClient


async def test_get_borrow_by_id(ac: AsyncClient):
    response = await ac.get("/borrows/1")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1
