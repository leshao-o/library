from httpx import AsyncClient


async def test_get_books(ac: AsyncClient):
    response = await ac.get(
        "/books",
        params={
            "page": 1,
            "per_page": 10
        }
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5
