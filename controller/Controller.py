from functools import wraps
from threading import Thread
from time import sleep

from .Input import Input
from .Invokation import Invokation
from .logging import Logger


class Controller(Logger):
    def __init__(self):
        super().__init__()

        self.kill = False
        self.reporter_thread = Thread(target=self.__reporter, args=())

        self.invokations = []

        # Report 10 times a second
        self.rate = 0.1

    def __reporter(self):
        while not self.kill:
            self.invoke()
            sleep(self.rate)

    def start(self):
        self.reporter_thread.start()

    def term(self):
        self.kill = True

        self.reporter_thread.join()

    def invoke(self):
        for key, input_ in self.__dict__.items():
            if isinstance(input_, Input):
                input_value = input_.invoke()
                if input_value is not None:
                    for invocation in self.invokations:
                        if invocation.is_(key):
                            invocation.invoke(input_value)

    def listen(self, *keys):
        def decorator(func):
            return self.__internal_listen(func, keys)

        return decorator

    def __internal_listen(self, func, key):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            return func(*args, **kwargs)

        if isinstance(key, tuple):
            for k in key:
                self.__bind(k, decorated_function)
        else:
            self.__bind(key, decorated_function)

        return decorated_function

    def __bind(self, key, func):
        self.invokations.append(Invokation(key, func))
