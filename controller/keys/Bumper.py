from controller.Input import Input


class Bumper(Input):
    def __init__(self, event):
        self.event_ = event
        self.interval = [0, 255]

    def validate(self, event):
        # event.ev_type, event.code, event.state
        return event.code == self.event_

    def parse(self, event):
        _, _, state_ = super().parse(event)

        return self.name, state_
