from controller.Input import Input


class Button(Input):
    def __init__(self, event):
        super().__init__()

        self.event_ = event

        self.state_ = False

    def validate(self, event):
        # event.ev_type, event.code, event.state
        return event.code == self.event_

    def parse(self, event):
        _, _, state_ = super().parse(event)

        self.state_ = bool(state_)

    def invoke(self):
        return self.state_
