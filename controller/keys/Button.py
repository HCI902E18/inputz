from .Input import Input


class Button(Input):
    def __init__(self, event):
        self.event_ = event

    def validate(self, code_):
        return code_ == self.event_

    def parse(self, state_):
        print(f'{self.name}!')
        return
