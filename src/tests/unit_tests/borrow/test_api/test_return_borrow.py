from httpx import AsyncClient


async def test_return_borrow(db, ac: AsyncClient):
    book = await db.book.get_by_id(id=1)
    # Количество доступных книг до того как вернули ее копию
    assert book.available_copies == 5

    response = await ac.patch(
        f"/borrows/1/return", 
        params={"return_date": "2024-12-20"}
    )  

    assert response.status_code == 200
    assert response.json()["data"]["return_date"] == "2024-12-20"

    book = await db.book.get_by_id(id=1)
    # Количество доступных книг после того как вернули ее копию
    assert book.available_copies == 6
