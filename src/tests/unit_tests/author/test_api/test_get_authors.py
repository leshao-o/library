from httpx import AsyncClient


async def test_get_authors(ac: AsyncClient, create_authors):
    response = await ac.get(
        "/authors",
        params={
            "page": 1,
            "per_page": 10
        }
    )
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5
