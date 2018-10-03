from inputs import devices

from .controllers import XboxController
from .logging import Logger


class Devices(Logger):
    def __init__(self):
        super().__init__()

        self.controllers = [
            XboxController
        ]

    def get_device(self):
        controllers_ = []
        for device in devices:
            self.log.debug(f"Found: {device.name}")

            for controller in self.controllers:
                if controller.validate(device.name):
                    controllers_.append(controller(device))

        if len(controllers_) == 0:
            self.log.info("No supported controller found.")
            exit(0)
        elif len(controllers_) > 1:
            return self.choose_device(controllers_)
        return controllers_[0]

    def choose_device(self, controllers):
        print("More then 1 device has been found, please choose controller to use.")

        for idx, device in enumerate(controllers):
            print(f"{idx}) {device.name}")

        while True:
            i = self.int_input("Enter device id:")

            if 0 <= i < len(controllers):
                return controllers[i]
            else:
                print("Number not within range.")

    def int_input(self, text):
        i = input(text)

        try:
            return int(i)
        except ValueError:
            print("Value is not an recognized integer")
            return self.int_input(text)

    def asdf(self):
        if len(devices) > 0:
            print("More then 1 device has been found, please choose controller to use.")

            for idx, device in enumerate(devices):
                print(f"{idx+1}) {device.name}")

            while True:
                i = int(input())
                print(devices[i - 1])
