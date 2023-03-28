class CheckOutProjectException(Exception):
    """Базовое исключение для проекта."""

class HTTPException(CheckOutProjectException):
    """Исключение при получении HTTP-ответа."""

class APIRequestError(CheckOutProjectException):
    """Неоднозначное исключение при обработке запроса API."""

class APIError(CheckOutProjectException):
    """Ответ сервера не равен 200."""

class JsonException(CheckOutProjectException):
    """Ошибка json метода."""
