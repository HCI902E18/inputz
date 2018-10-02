from .Input import Input


class Joystick(Input):
    def __init__(self, dir_x, dir_y):
        self.events_ = [dir_x, dir_y]
        self.dir_x_ = dir_x
        self.dir_y_ = dir_y

    def validate(self, code_):
        return code_ in self.events_

    def parse(self, state_):
        print(f'{self.name}!')
        return
