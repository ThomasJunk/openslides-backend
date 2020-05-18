class BackendBaseException(Exception):
    """
    Base exception for all custom exceptions of this service.
    """

    def __init__(self, message: str) -> None:
        self.message = message


class AuthenticationException(BackendBaseException):
    pass


class ViewException(BackendBaseException):
    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code


class ActionException(BackendBaseException):
    pass


class PresenterException(BackendBaseException):
    pass


class PermissionDenied(BackendBaseException):
    pass


class DatastoreException(BackendBaseException):
    pass


class EventStoreException(BackendBaseException):
    pass
