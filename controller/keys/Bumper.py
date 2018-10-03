from controller.Input import Input


class Bumper(Input):
    def __init__(self, event, offset=10):
        super().__init__()

        self.offset_ = offset / 100

        self.event_ = event
        self.interval = [0, 255]

        self.state_ = 0

    def validate(self, event):
        # event.ev_type, event.code, event.state
        return event.code == self.event_

    def parse(self, event):
        _, _, state_ = super().parse(event)

        val_ = 0
        if self.interval[0] <= state_ <= self.interval[1]:
            val_ = state_ / self.interval[1]

        if val_ < self.offset_:
            val_ = 0

        self.state_ = val_

    def invoke(self):
        if self.state_ == 0:
            return False
        return self.state_
