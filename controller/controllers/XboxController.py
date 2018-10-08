from threading import Thread

import keyboard as keybard

from controller.Controller import Controller
from controller.Input import Input
from controller.keys.Bumper import Bumper
from controller.keys.Button import Button
from controller.keys.Joystick import Joystick


class XboxController(Controller):
    @staticmethod
    def validate(name):
        return name == 'Microsoft X-Box 360 pad'

    @property
    def name(self):
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

        self.vibrating = False

    def read(self):
        return self.device.read()

    def __event_listener(self):
        while not self.kill:
            for event in self.read():
                self.parse(event)

    def start(self):
        super().start()

        self.event_listener_thread.start()

        while True:
            if keybard.is_pressed('Esc'):
                print("WE ARE EXITING NOW!")
                self.term()
                exit(0)

    def term(self):
        super().term()

        self.event_listener_thread.join()

    def parse(self, event):
        for _, input_ in self.__dict__.items():
            if isinstance(input_, Input):
                if input_.validate(event):
                    input_.parse(event)

    def vibrate(self, value):
        val = value

        self.device.set_vibration(
            val,
            val
        )
