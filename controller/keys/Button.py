from .Input import Input


class Button(Input):
    def __init__(self, event):
        self.event_ = event

    def validate(self, event):
        # event.ev_type, event.code, event.state
        return event.code == self.event_

    def parse(self, event):
        _, _, state_ = super().parse(event)

        if state_ == 1:
            return 'PUSHED'
        return 'RELEASED'
