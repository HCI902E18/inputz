from .logging import Logger


class Invokation(Logger):
    def __init__(self, key: str, func: "function"):
        super().__init__()

        self.key = key
        self.func = func

    def is_(self, key: str) -> bool:
        return self.key.upper() == key.upper()

    def transmit(self, value: object) -> None:
        if callable(self.func):
            self.func(value)
        else:
            raise Exception('Function is not callable')
