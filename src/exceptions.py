from datetime import date
from fastapi import HTTPException


def check_date(borrow_date: date, return_date: date) -> None:
    if return_date <= borrow_date:
        raise HTTPException(
            status_code=422, detail="Дата возврата не может быть раньше даты заема"
        )


class LibraryException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(LibraryException):
    detail = "Объект не найден"


class AuthorNotFoundException(ObjectNotFoundException):
    detail = "Автор не найден"


class BookNotFoundException(ObjectNotFoundException):
    detail = "Книга не найдена"


class BorrowNotFoundException(ObjectNotFoundException):
    detail = "Займ не найден"


class NoAvailableCopiesException(LibraryException):
    detail = "Нет доступных экземпляров книги для выдачи"


class BookAlreadyReturnedException(LibraryException):
    detail = "Книга уже была возвращена по этому займу"


class InvalidInputException(LibraryException):
    detail = "Некорректно введены данные"


class LibraryHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Объект не найден"


class AuthorNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Автор не найден"


class BookNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Книга не найдена"


class BorrowNotFoundHTTPException(ObjectNotFoundHTTPException):
    detail = "Займ не найден"


class NoAvailableCopiesHTTPException(LibraryHTTPException):
    status_code = 404
    detail = "Нет доступных экземпляров книги для выдачи"


class BookAlreadyReturnedHTTPException(LibraryHTTPException):
    status_code = 409
    detail = "Книга уже была возвращена по этому займу"


class InvalidInputHTTPException(LibraryHTTPException):
    status_code = 400
    detail = "Неверные введенные данные"
