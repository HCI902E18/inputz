import time
from queue import Queue
from time import sleep

import keyboard as keybard

from .Input import Input
from .KillableThread import KillableThread
from .invokations import Invokation
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

        # Tickrate of the reporter, 0.1 = 10 ticks a second
        self._tick_rate = 0.1

        # Functions or method called in case of controller disconnection
        self.__abort_methods = Queue()

        # Property used for thread killing in case of controller disconnection
        self.__self_destruct = False

        # Used for the controller to run in unsecure mode, which means that the decorated functions or classes
        # does not handle controller disconnection
        self.__unsecure = False

    def __reporter(self) -> None:
        """
        Thread method, checks in intervals what button are pressed.
        Runs while __killed == False

        :return: None
        """
        while not self.__kill:
            # Start tick
            start_time = time.time()

            self.__check_keys()

            # Calculate the time that the reporter should sleep
            sleep_time = self._tick_rate - (time.time() - start_time)

            # Handle too slow calculations
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                self.log.error(f"Tick took too long, skipping")

                overflow = round(abs(sleep_time), 5)
                self.log.debug(f"Tick overshoot by {overflow}ms")

    def start(self) -> None:
        """
        Method used to start all the threads

        :return: None
        """

        if self.__abort_methods.qsize() == 0 and not self.__unsecure:
            self.log.error("No abort method or functions found")
            self.log.error("These need to be handled in case of controller disconnection")
            self.log.error("OR run the controller in unsecure mode. (device.run_unsecure())")
            exit(1)

        for thread in self.__threads:
            thread.start()

    def __killer(self) -> None:
        """
        Killer thread
        This method is burning dem CPU cycles, but in return it's listening for that escape key

        :return: None
        """
        while True:
            if keybard.is_pressed('Esc') or self.__self_destruct:
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

    def method_listener(self, func: "function", keys) -> None:
        """
        Method for binding methods from other class instances

        :param func: The function to be called
        :param keys: Key as string or list
        :return: None
        """
        if isinstance(keys, list):
            for key in keys:
                self.__bind(func, key)
        else:
            self.__bind(func, keys)

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
        Allows controller, to make function calls via reporter

        :param func: The function to be called
        :param keys: Keys either as string or tuple
        :return: Returns the decorated function
        """

        if isinstance(keys, tuple):
            for key in keys:
                self.__bind(func, key)
        else:
            self.__bind(func, keys)

        return func

    def __bind(self, func: "function", key: str) -> None:
        """
        Binds the key to the function

        :param func: The function to bind
        :param key: Key as string
        :return: None
        """
        self.__invocations.append(Invokation(func, key))

    def kill_state(self) -> bool:
        """
        Getter for the private kill variable
        :return: is kill running?
        """
        return self.__kill

    def abort(self) -> None:
        """
        Methods which invokes ALL abort method and functions

        :return: None
        """
        # Sets the controller in self destruct mode so all threads are killed safe-fully
        self.__self_destruct = True

        # Call all methods in abort queue, called in FIFO order
        while self.__abort_methods.qsize() > 0:
            # Pop first method or function
            func = self.__abort_methods.get()

            # Call method or function
            func()

    def abort_method(self, method: "function") -> None:
        """
        Decorator for class methods which should be executed in case of a disconnect

        :param method: A method to be run when program aborts
        :return: None
        """
        self.__abort_methods.put(method)
        return

    def abort_function(self, func: "function") -> "function":
        """
        Decorator for function which should be executed in case of a disconnect

        :param func: A function to be run when program aborts
        :return: Returns the same function as given as parameter
        """
        self.__abort_methods.put(func)

        return func

    def run_unsecure(self) -> None:
        """
        Method which allows the controller to run with no method or functions to handle controller disconnection

        :return: None
        """
        self.__unsecure = True
