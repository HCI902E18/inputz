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
        self.RIGHT_STICK = Joystick('ABS_RX', 'ABS_RY')

        self.RIGHT_BUMPER = Bumper('ABS_RZ')
        self.LEFT_BUMPER = Bumper('ABS_Z')

    def start(self):
        while 1:
            for event in get_gamepad():
                self.parse(event.ev_type, event.code, event.state)

    def parse(self, _, code_, state_):
        for k, v in self.__dict__.items():
            if isinstance(v, Input):
                if v.validate(code_):
                    print(k, code_, state_)
