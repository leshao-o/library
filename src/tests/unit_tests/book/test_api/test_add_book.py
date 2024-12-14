from httpx import AsyncClient


async def test_add_book(ac: AsyncClient):
    title = "книга"
    description = "описание"
    author_id = 1
    available_copies = 5
    id = 6

    response = await ac.post(
        "/books",
        json={
            "title": title,
            "description": description,
            "author_id": author_id,
            "available_copies": available_copies,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "OK",
        "data": {
            "title": title,
            "description": description,
            "author_id": author_id,
            "available_copies": available_copies,
            "id": id,
        },
    }
