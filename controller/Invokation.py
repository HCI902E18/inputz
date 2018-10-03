from typing import TypeVar

from .logging import Logger

func_ = TypeVar('func_')


class Invokation(Logger):
    def __init__(self, key: str, func: func_):
        super().__init__()

        self.key = key
        self.func = func

    def is_(self, key: str) -> bool:
        return self.key.upper() == key.upper()

    def invoke(self, value: object) -> None:
        self.func(value)
