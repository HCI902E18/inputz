from .Input import Input


class Joystick(Input):
    def __init__(self, dir_x, dir_y):
        self.events_ = {
            dir_x: 0,
            dir_y: 0
        }

        self.interval = [-33000, 33000]
        self.vector = [0, 0]

    def validate(self, event):
        # event.ev_type, event.code, event.state
        for k, _ in self.events_.items():
            if k == event.code:
                return True
        return False
        # return event.code in self.events_

    def parse(self, event):
        _, code, state_ = super().parse(event)

        if state_ <= self.interval[0] or state_ >= self.interval[1]:
            print(code, state_)

        self.events_[code] = state_
        self.calculate()

        return self.vector

    def calculate(self):
        for key, (_, value) in enumerate(self.events_.items()):
            if value == 0:
                self.vector[key] = 0
            elif value > 0:
                self.vector[key] = int((value / self.interval[1]) * 100)
            elif value < 0:
                self.vector[key] = -int((abs(value) / abs(self.interval[0])) * 100)
