from .base import ExceptionBase


class NotFoundException(ExceptionBase):
    def __init__(self, msg):
        ExceptionBase.__init__(self, msg)
