from inputz.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A')
def test_func(args):
    print('test_func', args)
    return


class TestClass(object):
    def __init__(self):
        device.method_listener(self.test_method, 'A')

    def test_method(self, args):
        print('test_method', args)
        return


if __name__ == "__main__":
    t = TestClass()
    device.start()
