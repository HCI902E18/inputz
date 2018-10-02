from .Input import Input


class Bumper(Input):
    def __init__(self, event):
        self.event_ = event
        self.interval = [0, 255]

    def validate(self, code_):
        return code_ == self.event_

    def parse(self, state_):
        print(f'{self.name}!')
        return
