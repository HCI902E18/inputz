from inputs import InputEvent

from .logging import Logger


class Input(Logger):
    @property
    def name(self):
        return self.__class__.__name__.upper()

    def validate(self, event):
        raise NotImplemented()

    def parse(self, event):
        if not isinstance(event, InputEvent):
            raise Exception('WRONG INPUT TYPE')
        return event.ev_type, event.code, event.state
