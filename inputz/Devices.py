from inputs import devices

from .Controller import Controller
from .controllers import XboxController
from .logging import Logger


class Devices(Logger):
    """
    Loads the devices which can be recognized by the libaries, and maps to local controller classes.
    """

    def __init__(self):
        super().__init__()

        # List of all controllers which can be mapped
        self.controllers = [
            # Xbox controller
            XboxController,
        ]

    def get_device(self):
        """
        Returns the device which should be used.
        If no device is connected this WILL kill the program.
        If multiple controllers connected, the users will be promoted to choose controller.

        :return: instance of the controller which is going to be used.
        """
        # List of all found controllers
        _controllers = []

        # Iterate through all controllers found by `inputs`
        for device in devices:
            self.log.debug(f"Found: {device.name}")

            for controller in self.controllers:
                # Checks if the device found by `inputs` is available as controller instance
                if controller.validate(device.name):
                    _controllers.append(controller(device))

        # Checks if any controllers were found
        if len(_controllers) == 0:
            self.log.error("No supported controller found.")
            exit(0)

        # Handle the case where multiple controllers were found
        elif len(_controllers) > 1:
            return self.choose_device(_controllers)

        # If only one controller found, return this
        return _controllers[0]

    def choose_device(self, controllers: list) -> Controller:
        """
        Allows for the user to choose between a list of controllers

        :param controllers: List of class instances of controllers
        :return: The controller which is going to be used
        """
        self.log.info("More then 1 device has been found, please choose controller to use.")

        for idx, device in enumerate(controllers):
            self.log.info(f"{idx}) {device.name}")

        while True:
            # Get's the users input
            i = self.int_input("Enter device id:")

            # Checks if the chosen controller is within the list
            if 0 <= i < len(controllers):

                # Returns the chosen controller
                return controllers[i]
            else:
                self.log.info("Number not within range.")

    def int_input(self, text: str) -> int:
        """
        Assures that the user input is an integer

        :param text: The text which is displayed next to the user input.
        :return: The number the user has chosen
        """
        i = input(text)

        try:
            return int(i)
        except ValueError:
            self.log.info("Value is not an recognized integer")

            # Recursive, until the user has chosen an integer
            return self.int_input(text)
