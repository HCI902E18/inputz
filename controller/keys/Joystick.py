from controller.Input import Input


class Joystick(Input):
    def __init__(self, dir_x, dir_y, offset=15):
        super().__init__()

        self.offset_ = offset / 100
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

    def parse(self, event):
        _, code, state_ = super().parse(event)

        if state_ <= self.interval[0] or state_ >= self.interval[1]:
            print(code, state_)

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
        if self.vector == [0, 0]:
            return False
        return self.vector
