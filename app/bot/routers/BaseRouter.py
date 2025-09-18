from abc import ABC, abstractmethod
from aiogram import Router


class BaseRouter(ABC):
    def __init__(self):
        self.router = Router()
        self._register_handlers()

    @abstractmethod
    def _register_handlers(self):
        pass
