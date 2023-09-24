from typing import Any

from handler.handler import Handler
from abc import abstractmethod


class AbstractHandler(Handler):
    """
    The default chaining behavior can be implemented inside a base handler
    class.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: Any) -> dict:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None
