from threading import Thread
from time import sleep

from inputs import get_gamepad

from .keys.Bumper import Bumper
from .keys.Button import Button
from .keys.Input import Input
from .keys.Joystick import Joystick


class Controller(object):
    def __init__(self):
        # Controller interactions
        self.A = Button('BTN_SOUTH')
        self.B = Button('BTN_EAST')
        self.X = Button('BTN_WEST')
        self.Y = Button('BTN_NORTH')

        self.START = Button('BTN_SELECT')
        self.SELECT = Button('BTN_START')

        self.RIGHT_TRIGGER = Button('BTN_TR')
        self.LEFT_TRIGGER = Button('BTN_TL')

        self.ARROWS = Joystick('ABS_HAT0X', 'ABS_HAT0Y')

        self.LEFT_STICK = Joystick('ABS_X', 'ABS_Y')
        self.LEFT_STICK_BUTTON = Button('BTN_THUMBL')
        self.RIGHT_STICK = Joystick('ABS_RX', 'ABS_RY')
        self.RIGHT_STICK_BUTTON = Button('BTN_THUMBR')

        self.RIGHT_BUMPER = Bumper('ABS_RZ')
        self.LEFT_BUMPER = Bumper('ABS_Z')

        self.kill = False
        self.reporter_thread = Thread(target=self.reporter, args=(self,))
        self.event_listener_thread = Thread(target=self.event_listener, args=(self,))

    @staticmethod
    def reporter(self):
        while not self.kill:
            sleep(0.1)

    @staticmethod
    def event_listener(self):
        while not self.kill:
            for event in get_gamepad():
                self.parse(event)

    def start(self):
        self.reporter_thread.start()
        self.event_listener_thread.start()

    def term(self):
        self.kill = True
        self.reporter_thread.join()
        self.event_listener_thread.join()

    def parse(self, event):
        for k, v in self.__dict__.items():
            if isinstance(v, Input):
                if v.validate(event):
                    print(k, v.parse(event))
