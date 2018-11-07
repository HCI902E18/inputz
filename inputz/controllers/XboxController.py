import enum
from copy import deepcopy

from inputs import UnpluggedError, InputEvent

from inputz.Controller import Controller
from inputz.Input import Input
from inputz.KillableThread import KillableThread
from inputz.OS import OS
from inputz.keys import Bumper
from inputz.keys.Button import Button
from inputz.keys.Joystick import Joystick


class XboxController(Controller):
    """
    Xbox controller mappings

    """

    @staticmethod
    def validate(name: str) -> bool:
        """
        Used to validate if the name of the controller matches this controller

        :param name: The name of the input controller
        :return: bool, if the controller matches
        """
        return name == 'Microsoft X-Box 360 pad'

    @property
    def name(self) -> str:
        """
        Gets the name of the connected device

        :return: String, name of device
        """
        return self.device.name

    def __init__(self, device):
        # Needs for logger to start
        super().__init__()

        # Which device this controller listen on
        self.device = device

        # Maps all the buttons on the controller
        self.A = Button('BTN_SOUTH')
        self.B = Button('BTN_EAST')
        self.X = Button('BTN_WEST')
        self.Y = Button('BTN_NORTH')

        self.START = Button(self.reverse_binding(win='BTN_SELECT', linux='BTN_START'))
        self.SELECT = Button(self.reverse_binding(win='BTN_START', linux='BTN_SELECT'))

        self.RIGHT_TRIGGER = Button('BTN_TR')
        self.LEFT_TRIGGER = Button('BTN_TL')

        self.ARROWS = Joystick('ABS_HAT0X', 'ABS_HAT0Y', interval=[-1, 1])

        self.LEFT_STICK = Joystick('ABS_X', 'ABS_Y', parse_func=self.joystick_linux_converter)
        self.LEFT_STICK_BUTTON = Button('BTN_THUMBL')
        self.RIGHT_STICK = Joystick('ABS_RX', 'ABS_RY', parse_func=self.joystick_linux_converter)
        self.RIGHT_STICK_BUTTON = Button('BTN_THUMBR')

        self.RIGHT_BUMPER = Bumper('ABS_RZ', interval=self.os_interval())
        self.LEFT_BUMPER = Bumper('ABS_Z', interval=self.os_interval())

        # This controller needs a thread which listens for controller inputs
        self.add_thread(KillableThread(name="ControllerThread", target=self.__event_listener, args=()))

        # Vibration vector
        self.vibrate_state = [0, 0]

    class Side(enum.Enum):
        left = 0
        right = 1

    def os_interval(self):
        if self.os == self.OS.linux:
            return [0, 1023]
        return [0, 255]

    def joystick_linux_converter(self, value):
        if self.os == self.OS.linux:
            value[1] = -value[1]
        return value

    def reverse_binding(self, **kwargs):
        if self.os == self.OS.win:
            return kwargs.get('win')
        elif self.os == self.OS.linux:
            return kwargs.get('linux')
        raise Exception('Mac is not yet supported')

    def read(self) -> list:
        """
        Method used for reading the input from the controller

        :return: list, the events from inputs on controller
        """
        try:
            return self.device.read()
        except UnpluggedError:
            # In case of disconnection, ABORT EVERYTHING
            self.abort()

            # If controller looses connection, this will catch it.
            self.log.error("The controller has been unplugged, application terminating")
            exit(1)

    def __event_listener(self) -> None:
        """
        Thread method which handles all events from controller

        :return: None
        """
        while not self.kill_state():
            for event in self.read():
                self.log.debug(event.code)
                self.parse(event)

    def parse(self, event: InputEvent) -> None:
        """
        Parser for controller events, tests whether the event belongs to a specific input

        :param event: the event from the controller
        :return: None
        """

        # We iterate through all properties on the class it self.
        for _, cls_prop in self.__dict__.items():
            # Checks if the property is instance of input
            if isinstance(cls_prop, Input):
                # Checks if the event belongs to this property
                if cls_prop.validate(event):
                    # Parse the event according to the input
                    cls_prop.parse(event)

    def vibrate(self, value: list) -> None:
        """
        Method used for vibrating the entire controller

        :param value: list of vibration level, scale is 0..1
        :return: None
        """
        if not isinstance(value, list) or len(value) != 2:
            self.log.warn("Invalid vibration format")
            return
        self.set_vibrate(value)

    def vibrate_left(self, value: int) -> None:
        """
        Method for vibrate only the left site of the controller

        :param value: Integer value, 0..1
        :return: None
        """
        self.set_vibrate(value, self.Side.left)

    def vibrate_right(self, value: int) -> None:
        """
        Method for vibrate only the right site of the controller

        :param value: Integer value, 0..1
        :return: None
        """
        self.set_vibrate(value, self.Side.right)

    def set_vibrate(self, value, side=None) -> None:
        """
        Sets the vibration value in vibration state

        :param value: The value for the vibration state
        :param side: The side of the controller
        :return: None
        """
        if isinstance(side, self.Side):
            self.vibrate_state[side.value] = value
        elif isinstance(value, list):
            # We need deep copy, not the reference
            self.vibrate_state = deepcopy(value)

        # Send the update to the controller
        self.update_vibrate()

    def update_vibrate(self) -> None:
        """
        Send the vibration state to the controller

        :return: None
        """
        if OS.WIN:
            self.device._start_vibration_win(*self.vibrate_state)
        elif OS.NIX:
            # untested!
            self.device._set_vibration_nix(*self.vibrate_state, 1000)
