from .base import ExceptionBase


class ClientException(ExceptionBase):
    pass


class ClientErrorException(ClientException):
    pass


class ServerErrorException(ClientException):
    pass
