class Input(object):
    def validate(self, code_):
        raise NotImplemented()

    @property
    def name(self):
        return self.__class__.__name__.upper()
