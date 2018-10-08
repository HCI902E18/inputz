from copy import deepcopy

from controller.Input import Input


class Joystick(Input):
    def __init__(self, dir_x, dir_y, **kwargs):
        super().__init__()

        self.offset_ = kwargs.get('offset', 15) / 100
        self.events_ = {
            dir_x: 0,
            dir_y: 0
        }

        self.default_vector = [0, 0]

        self.interval = deepcopy(kwargs.get('interval', [-32767, 32767]))
        self.vector = deepcopy(self.default_vector)
        self.last_report_ = deepcopy(self.default_vector)

    def validate(self, event):
        # event.ev_type, event.code, event.state
        for k, _ in self.events_.items():
            if k == event.code:
                return True
        return False

    def parse(self, event):
        _, code, state_ = super().parse(event)

        if state_ < self.interval[0] or state_ > self.interval[1]:
            self.log.error(f"{code}, {state_}")

        self.events_[code] = state_
        self.calculate()

        return self.vector

    def calculate(self):
        for key, (_, value) in enumerate(self.events_.items()):
            val_ = self.calc_vector_value(value)
            if abs(val_) < self.offset_:
                self.vector[key] = 0
            else:
                self.vector[key] = val_

    def calc_vector_value(self, value):
        if value == 0:
            return 0
        elif value > 0:
            return self.percentage(value, self.interval[1])
        elif value < 0:
            return -(self.percentage(value, self.interval[0]))

    @staticmethod
    def percentage(value, max_):
        return abs(value) / abs(max_)

    def invoke(self):
        if self.vector == self.last_report_ == self.default_vector:
            return None
        return self.set_last_report_(self.vector)
