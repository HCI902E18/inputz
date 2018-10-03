from threading import Thread
from time import sleep

from .Input import Input
from .logging import Logger


class Controller(Logger):
    def __init__(self):
        super().__init__()

        self.kill = False
        self.reporter_thread = Thread(target=self.__reporter, args=())

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
                    print(f"INVOKE {key}")
