from copy import deepcopy
from threading import Thread

import keyboard as keybard
from inputs import UnpluggedError

from controller.Controller import Controller
from controller.Input import Input
from controller.keys.Bumper import Bumper
from controller.keys.Button import Button
from controller.keys.Joystick import Joystick


class XboxController(Controller):
    @staticmethod
    def validate(name: str) -> bool:
        return name == 'Microsoft X-Box 360 pad'

    @property
    def name(self) -> str:
        return self.device.name

    def __init__(self, device):
        # Needs for logger to start
        super().__init__()

        # Which device this controller listen on
        self.device = device

        # Controller interactions
        self.A = Button('BTN_SOUTH')
        self.B = Button('BTN_EAST')
        self.X = Button('BTN_WEST')
        self.Y = Button('BTN_NORTH')

        self.START = Button('BTN_SELECT')
        self.SELECT = Button('BTN_START')

        self.RIGHT_TRIGGER = Button('BTN_TR')
        self.LEFT_TRIGGER = Button('BTN_TL')

        self.ARROWS = Joystick('ABS_HAT0X', 'ABS_HAT0Y', interval=[-1, 1])

        self.LEFT_STICK = Joystick('ABS_X', 'ABS_Y')
        self.LEFT_STICK_BUTTON = Button('BTN_THUMBL')
        self.RIGHT_STICK = Joystick('ABS_RX', 'ABS_RY')
        self.RIGHT_STICK_BUTTON = Button('BTN_THUMBR')

        self.RIGHT_BUMPER = Bumper('ABS_RZ')
        self.LEFT_BUMPER = Bumper('ABS_Z')

        self.event_listener_thread = Thread(target=self.__event_listener, args=())

        self.vibrate_state = [0, 0]

    def read(self):
        try:
            return self.device.read()
        except UnpluggedError:
            self.log.error("The controller has been unplugged")
            exit(1)

    def __event_listener(self):
        while not self.kill_state():
            for event in self.read():
                self.parse(event)

    def start(self):
        super().start()

        self.event_listener_thread.start()

        while True:
            if keybard.is_pressed('Esc'):
                print("WE ARE EXITING NOW!")
                self.terminate()
                exit(0)

    def terminate(self):
        super().terminate()

        self.event_listener_thread.join()

    def parse(self, event):
        for _, input_ in self.__dict__.items():
            if isinstance(input_, Input):
                if input_.validate(event):
                    input_.parse(event)

    def vibrate(self, value: list):
        if not isinstance(value, list) or len(value) != 2:
            return
        self.set_vibrate(deepcopy(value))

    def vibrate_left(self, value: int):
        self.set_vibrate(value, 0)

    def vibrate_right(self, value: int):
        self.set_vibrate(value, 1)

    def set_vibrate(self, value, idx=None):
        if idx is None:
            self.vibrate_state = value
        else:
            self.vibrate_state[idx] = value
        self.update_vibrate()

    def update_vibrate(self):
        self.device.set_vibration(*self.vibrate_state)
