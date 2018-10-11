from inputz.Devices import Devices


class TestClass(object):
    def __init__(self):
        self.device = Devices().get_device()

        self.device.method_listener(self.test_method, 'A')

    def test_method(self, args):
        print('test_method', args)
        return

    def start(self):
        self.device.start()


if __name__ == "__main__":
    t = TestClass()
    t.start()
