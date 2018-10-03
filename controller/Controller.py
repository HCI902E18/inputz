from functools import wraps
from threading import Thread
from time import sleep

from .Input import Input
from .logging import Logger


class Controller(Logger):
    def __init__(self):
        super().__init__()

        self.kill = False
        self.reporter_thread = Thread(target=self.__reporter, args=())

        self.event_listeners = []

    def __reporter(self):
        while not self.kill:
            self.invoke()
            sleep(0.1)

    def start(self):
        self.reporter_thread.start()

    def term(self):
        self.kill = True

        self.reporter_thread.join()

    def invoke(self):
        for key, input_ in self.__dict__.items():
            if isinstance(input_, Input):
                if input_.invoke():
                    for event in self.event_listeners:
                        if event['key'] == key:
                            event['func']()

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
        self.event_listeners.append({
            'key': key,
            'func': func
        })
