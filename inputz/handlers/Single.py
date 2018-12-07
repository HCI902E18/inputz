from .Handler import Handler


class Single(Handler):
    def __init__(self):
        self.last_value = False
        return

    def should_emit(self, value):
        if self.last_value == value:
            return False

        self.last_value = value
        return True
