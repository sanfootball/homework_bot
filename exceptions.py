class CheckOutProjectException(Exception):
    """Базовое исключение для проекта."""

class APIRequestError(CheckOutProjectException):
    """Неоднозначное исключение при обработке запроса API."""

class APIError(CheckOutProjectException):
    """Ответ сервера не равен 200."""

class JsonException(CheckOutProjectException):
    """Ошибка json метода."""
