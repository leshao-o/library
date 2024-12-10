from fastapi import APIRouter, Body

from src.exceptions import AuthorNotFoundException, AuthorNotFoundHTTPException, InvalidInputException, InvalidInputHTTPException
from src.services.author import AuthorService
from src.api.dependencies import DBDep, PaginationDep
from src.schemas.author import AuthorAdd, AuthorPatch


router = APIRouter(prefix="/authors", tags=["Авторы"])


@router.post(
    "",
    summary="Добавляет автора",
    description=(
        """Этот эндпоинт добавляет нового автора в базу данных. 
        Ожидает имя, фамилию и дату рождения автора. 
        Возвращает статус операции и данные нового автора."""
    )
)
async def add_author(
    db: DBDep, 
    author_data: AuthorAdd = Body(
        openapi_examples={
            "1": {
                "summary": "author_1",
                "value": {
                    "first_name": "Александр", 
                    "last_name": "Пушкин", 
                    "birth_date": "1799-06-06"
                },
            },
            "2": {
                "summary": "author_2",
                "value": {
                    "first_name": "Лев", 
                    "last_name": "Толстой", 
                    "birth_date": "1828-09-09"
                },
            }
        }
    )
):
    new_author = await AuthorService(db).create_author(author_data=author_data)
    return {"status": "OK", "data": new_author}


@router.get(
    "",
    summary="Получает список всех авторов",
    description=(
        """Этот эндпоинт возвращает список всех авторов из базы данных. 
        Ожидает количество авторов на странице и номер страницы. 
        Возвращает статус операции и данные авторов для указанной страницы."""
    )
)
async def get_all_authors(db: DBDep, pagination: PaginationDep):
    try:
        authors = await AuthorService(db).get_all_authors()
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    authors = authors[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return {"status": "OK", "data": authors}


@router.get(
    "/{id}",
    summary="Получает данные конкретного автора",
    description=(
        """Этот эндпоинт возвращает информацию об авторе по его уникальному идентификатору. 
        Ожидает ID автора. 
        Возвращает статус операции и данные запрашиваемого автора."""
    )
)
async def get_author_by_id(db: DBDep, id: int):
    try:
        author = await AuthorService(db).get_author_by_id(id=id)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    return {"status": "OK", "data": author}


@router.put(
    "/{id}",
    summary="Обновляет данные конкретного автора",
    description=(
        """Этот эндпоинт редактирует информацию об авторе по его уникальному идентификатору. 
        Ожидает ID автора и необязательные данные для обновления: имя, фамилию и дату рождения. 
        Возвращает статус операции и данные автора c обновленными значениями."""
    )
)
async def edit_author(
    db: DBDep, 
    id: int,
    author_data: AuthorPatch = Body(
        openapi_examples={
            "1": {
                "summary": "author_1",
                "value": { 
                    "last_name": "Грибоедов", 
                    "birth_date": "1795-01-15"
                },
            },
            "2": {
                "summary": "author_2",
                "value": {
                    "first_name": "Михаил", 
                    "last_name": "Ломоносов", 
                    "birth_date": "1711-11-19"
                },
            }
        }
    )
):
    try:
        edited_author = await AuthorService(db).edit_author(id=id, author_data=author_data)
    except InvalidInputException:
        raise InvalidInputHTTPException
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    return {"status": "OK", "data": edited_author}


@router.delete(
    "/{id}",
    summary="Удаляет автора по его уникальному идентификатору",
    description=(
        """Этот эндпоинт удаляет автора из базы данных по его уникальному идентификатору. 
        Ожидает ID автора. 
        Возвращает статус операции и данные удаленного автора."""
    )
)
async def delete_author(db: DBDep, id: int):
    try:
        deleted_author = await AuthorService(db).delete_author(id=id)
    except AuthorNotFoundException:
        raise AuthorNotFoundHTTPException
    return {"status": "OK", "data": deleted_author}
