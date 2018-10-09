from copy import deepcopy

from inputs import InputEvent

from inputz.Input import Input


class Bumper(Input):
    """
    Class mapping to X-Box Bumpers
    """

    def __init__(self, event, **kwargs):
        super().__init__()

        # Bumper might wobble, so this value is to filter those
        self.__offset = kwargs.get('offset', 0) / 100

        # This is the event the bumper will listen for
        self.__event = event
        # The interval the event will be within
        self.interval = deepcopy(kwargs.get('interval', [0, 255]))

        # The current state of the bumper
        self.__state = 0
        # The last value the bumper reported to functions listen for it
        self._last_report = 0

    def validate(self, event) -> bool:
        """
        Validates if this event is for this bumper

        :param event: Event from the controller
        :return: bool
        """
        if not isinstance(event, InputEvent): return False
        return event.code == self.__event

    def parse(self, event) -> None:
        """
        Parse the event to get data for this bumper.

        :param event: The event which data should be extracted from.
        :return: None
        """
        if not isinstance(event, InputEvent): return
        _, _, state_ = super().parse(event)

        val_ = 0

        # Checks that the event value is between the interval
        if self.interval[0] <= state_ <= self.interval[1]:
            val_ = state_ / self.interval[1]

        # If the value is within the wobble boundary, remove
        if val_ < self.__offset:
            val_ = 0

        self.__state = val_

    def value(self) -> float:
        """
        Method that returns the value of the bumper.
        Returns the value if the value changed since last report
        Else report `None`

        :return: None or float
        """
        if self.__state == self._last_report and self.__state == 0:
            return None
        return self._set_last_report(self.__state)
