from functools import wraps
from time import sleep

import keyboard as keybard

from .Input import Input
from .Invokation import Invokation
from .KillableThread import KillableThread
from .logging import Logger


class Controller(Logger):
    """
    Controller

    Generic class for each controller to implement.
    Spawns reporter thread, thread is used to call methods which listens for button presses.
    """

    def __init__(self):
        super().__init__()

        # Used as thread loop condition
        self.__kill = False

        # Thread used for reporter
        self.killer_thread = 'tronald_dump'

        self.__threads = [
            KillableThread(name='reporter', target=self.__reporter, args=()),
            KillableThread(name=self.killer_thread, target=self.__killer, args=())
        ]

        # List of functions waiting for event to trigger
        self.__invocations = []

        # Report 10 times a second
        self.__rate = 0.1

    def __reporter(self) -> None:
        """
        Thread method, checks in intervals what button are pressed.
        Runs while __killed == False

        :return: None
        """
        while not self.__kill:
            self.__check_keys()
            sleep(self.__rate)

    def start(self) -> None:
        """
        Method used to start all the threads

        :return: None
        """
        for thread in self.__threads:
            thread.start()

    def __killer(self) -> None:
        """
        Killer thread
        This method is burning dem CPU cycles, but in return it's listening for that escape key

        :return: None
        """
        while True:
            if keybard.is_pressed('Esc'):
                print("WE ARE EXITING NOW!")
                self.terminate()
                exit(0)

    def add_thread(self, thread: KillableThread) -> bool:
        """
        A contoller may run multiple threads in order to keep track of multiple I/O operations

        :param thread: The thread which should be added to the pool
        :return: Boolean if the thread is added
        """
        if isinstance(thread, KillableThread):
            self.__threads.append(thread)
            return True
        return False

    def terminate(self) -> None:
        """
        Method used for politely killing reporter threads

        :return: None
        """
        self.__kill = True

        for thread in self.__threads:
            # A thread cannot kill it self, but this specific thread kills it self anyway
            if thread.name != self.killer_thread:
                thread.kill(consequences=True)

    def __check_keys(self) -> None:
        """
        Checks all properties which is of the instance Input.Input.
        If Input is not `None` report that value to functions which is listening for it.

        :return: None
        """

        # Loops over all properties of self class instance
        for key, input_ in self.__dict__.items():

            # Checks if property is of instance Input.Input
            if isinstance(input_, Input):

                # Gets the value from the controller key
                input_value = input_.value()

                # If key is not `None`, send value to functions which is listening
                if input_value is not None:

                    # Loops over all invocations
                    for invocation in self.__invocations:

                        # Checks if invocations is listening for current key
                        if invocation.is_(key):
                            # Transmit value to invocation
                            invocation.transmit(input_value)

    def listen(self, *keys) -> "function":
        """
        Decorator for functions

        :param keys: Which keys should trigger the function
        :return: Decorated function
        """

        def decorator(func):
            return self.__internal_listen(func, keys)

        return decorator

    def __internal_listen(self, func: "function", keys) -> "function":
        """
        Internal function decorator, maps one to many keys to one function

        :param func: The function to be decorated
        :param keys: Keys either as string or tuple
        :return: Returns the decorated function
        """

        @wraps(func)
        def decorated_function(*args, **kwargs):
            return func(*args, **kwargs)

        # If keys is list, map function to all keys
        if isinstance(keys, tuple):
            for key in keys:
                self.__bind(key, decorated_function)
        else:
            self.__bind(keys, decorated_function)

        return decorated_function

    def __bind(self, key: str, func: "function") -> None:
        """
        Binds the key to the function

        :param key: Key as string
        :param func: The function to bind
        :return: None
        """
        self.__invocations.append(Invokation(key, func))

    def kill_state(self) -> bool:
        """
        Getter for the private kill variable
        :return: is kill running?
        """
        return self.__kill
