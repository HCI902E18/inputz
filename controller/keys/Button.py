from inputs import InputEvent

from controller.Input import Input


class Button(Input):
    """
    Class mapping to X-Box Buttons
    """

    def __init__(self, event):
        super().__init__()

        # This is the event the button will listen for
        self.__event = event

        # The current state of the button
        self.__state = False
        # The last value the button reported to functions listen for it
        self._last_report = False

    def validate(self, event: InputEvent) -> bool:
        """
        Validates if this event is for this button

        :param event: Event from the controller
        :return: bool
        """
        if not isinstance(event, InputEvent): return False
        return event.code == self.__event

    def parse(self, event) -> None:
        """
        Parse the event to get data for this button.

        :param event: The event which data should be extracted from.
        :return: None
        """
        if not isinstance(event, InputEvent): return
        _, _, state_ = super().parse(event)

        self.__state = bool(state_)

    def value(self) -> bool:
        """
        Method that returns the value of the button.
        Returns the value if the value changed since last report
        Else report `None`

        :return: None or bool
        """
        if self.__state == self._last_report and not self.__state:
            return None
        return self._set_last_report(self.__state)
