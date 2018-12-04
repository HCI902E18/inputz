class button(object):
    def __init__(self, f):
        self.f = f
        self.state = False

    def __call__(self, *args):
        if len(args) == 0:
            self.f(*args)

        if self.state != args[0]:
            self.state = args[0]
            self.f(*args)
