from httpx import AsyncClient


async def test_add_borrow(db, ac: AsyncClient):
    book_id = 1
    reader_name = "Андрей"
    borrow_date = "2024-12-10"
    id = 6
    return_date = None

    book = await db.book.get_by_id(id=1)
    # Количество доступных книг до добавления займа
    assert book.available_copies == 5

    response = await ac.post(
        "/borrows",
        json={
            "book_id": book_id,
            "reader_name": reader_name,
            "borrow_date": borrow_date,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "OK",
        "data": {
            "book_id": book_id,
            "reader_name": reader_name,
            "borrow_date": borrow_date,
            "id": id,
            "return_date": return_date,
        },
    }

    book = await db.book.get_by_id(id=1)
    # Количество доступных книг после добавления займа
    assert book.available_copies == 4
