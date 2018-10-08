from copy import deepcopy

from inputs import InputEvent

from .logging import Logger


class Input(Logger):
    def __init__(self):
        super().__init__()

        self.last_update = 0
        self.last_report_ = None

    @property
    def name(self):
        return self.__class__.__name__.upper()

    def validate(self, event):
        raise NotImplemented()

    def parse(self, event):
        if not isinstance(event, InputEvent):
            raise Exception('WRONG INPUT TYPE')
        self.update_time(event)
        return event.ev_type, event.code, event.state

    def update_time(self, event):
        self.last_update = event.timestamp

    def set_last_report_(self, report):
        # Deepcopy is needed in case of vector (list of two elements)
        self.last_report_ = deepcopy(report)
        return report

    def value(self):
        raise NotImplemented()
