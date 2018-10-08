from copy import deepcopy

from inputs import InputEvent

from .logging import Logger


class Input(Logger):
    """
    Input

    Base class for all input types
    """

    def __init__(self):
        super().__init__()

        # The value from last time the input was read
        self.last_report_ = None

    def validate(self, event: InputEvent) -> Exception:
        """
        Checks if current event is related to this input

        :param event: The event and data related to
        :return: This is just a base class so this will throw exception
        """
        raise NotImplemented()

    def parse(self, event):
        """
        Method used for parsing the event
        :param event: The InputEvent
        :return: Type, Code And state of the input
        """
        if not isinstance(event, InputEvent):
            raise Exception('WRONG INPUT TYPE')
        return event.ev_type, event.code, event.state

    def set_last_report_(self, report):
        # Deepcopy is needed in case of vector (list of two elements)
        self.last_report_ = deepcopy(report)
        return report

    def value(self):
        """
        The value of the input

        :return: The value of the input
        """
        raise NotImplemented()
