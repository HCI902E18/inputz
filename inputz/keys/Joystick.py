from copy import deepcopy

from inputs import InputEvent

from inputz.Input import Input


class Joystick(Input):
    """
    Class mapping to X-Box Joystick
    """

    def __init__(self, direction_x, direction_y, **kwargs):
        super().__init__()

        # Bumper might wobble, so this value is to filter those
        self.offset_ = kwargs.get('offset', 15) / 100

        # Joysticks move in two direction, these are mapped as a dictionary
        self.__event = {
            direction_x: 0,
            direction_y: 0
        }

        # Default vector used checking for None values
        self.default_vector = [0, 0]

        # The interval the event will be within
        self.interval = deepcopy(kwargs.get('interval', [-32768, 32767]))
        # The current joystick vector
        self.vector = deepcopy(self.default_vector)

        # The last value the joystick reported to functions listen for it
        self._last_report = deepcopy(self.default_vector)

    def validate(self, event) -> bool:
        """
        Validates if this event is for this joystick

        :param event: Event from the controller
        :return: bool
        """
        if not isinstance(event, InputEvent): return False
        for k, _ in self.__event.items():
            if k == event.code:
                return True
        return False

    def parse(self, event) -> None:
        """
        Parse the event to get data for this joystick.

        :param event: The event which data should be extracted from.
        :return: None
        """
        if not isinstance(event, InputEvent): return
        _, code, value = super().parse(event)

        if value < self.interval[0] or value > self.interval[1]:
            self.log.error(f"{code}, {value}")

        # Map the value to the direction of the joystick
        self.__event[code] = value

        # Recalculate the vector
        self.calculate()

    def calculate(self) -> None:
        """
        Calculate the joystick vector

        :return: None
        """
        # Iterate through the directions of the joystick
        for key, (_, value) in enumerate(self.__event.items()):
            # Calculate the vector value
            val_ = self.calc_vector_value(value)

            # Handle wobble offset
            if abs(val_) < self.offset_:
                self.vector[key] = 0
            else:
                self.vector[key] = val_

    def calc_vector_value(self, value: int) -> float:
        """
        Calculate the percentage vector in +/- directions

        :param value: Value from the event
        :return: percent direction
        """

        if value == 0:
            return 0
        else:
            return self.percentage(value, self.interval[1 if value > 0 else 0])

    @staticmethod
    def percentage(value: int, _max: int) -> float:
        """
        Calculate positive percentage from absolute values

        :param value: The value of the numerator
        :param _max: The value of the denominator
        :return: float
        """
        return value / abs(_max)

    def value(self) -> list:
        """
        Method that returns the value of the joystick.
        Returns the value if the value changed since last report
        Else report `None`

        :return: None or list
        """
        if self.vector == self._last_report == self.default_vector:
            return None
        return self._set_last_report(self.vector)
