from .Handler import Handler


class Contentious(Handler):
    def should_emit(self, value):
        return True
