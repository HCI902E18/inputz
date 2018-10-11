from inputz.logging import Logger


class Invokation(Logger):
    """
    Class used for triggering functions through bindings
    """

    def __init__(self, func: "function", key: str):
        super().__init__()

        self.func = func
        self.key = key

    def is_(self, key: str) -> bool:
        """
        Checks if the key should trigger the function related to this invokation

        :param key: The currently pressed key as string
        :return: boolean, true if key is this key
        """
        return self.key.upper() == key.upper()

    def transmit(self, value: object) -> None:
        """
        Method used for sending data to functions

        :param value: The value which should be passed on to the function
        :param cls: The class which the method may belong to
        :return: None
        """
        if callable(self.func):
            self.func(value)
        else:
            raise Exception('Function is not callable')
