from threading import Thread
from time import sleep

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

        self.device = device

        self.kill = False
        self.reporter_thread = Thread(target=self.__reporter, args=())
        self.event_listener_thread = Thread(target=self.__event_listener, args=())

    def __reporter(self):
        while not self.kill:
            sleep(0.1)

    def __event_listener(self):
        while not self.kill:
            for event in self.device.read():
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
