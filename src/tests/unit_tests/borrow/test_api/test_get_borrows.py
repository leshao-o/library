from httpx import AsyncClient


async def test_get_borrows(ac: AsyncClient):
    response = await ac.get(
        "/borrows", 
        params={"page": 1, "per_page": 10}
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5
