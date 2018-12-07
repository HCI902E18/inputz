from inputz.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A', handler=device.Handler.single)
def test_func(args):
    print('test_func', args)
    return


@device.abort_function
def abort():
    print("TEST FUNCTION ABORTING")
    return


class TestClass(object):
    def __init__(self):
        device.method_listener(self.test_method, 'A', device.Handler.single)

        device.abort_method(self.abort)

    def test_method(self, args):
        print('test_method', args)
        return

    def abort(self):
        print("TEST CLASS ABORTING")
        return


if __name__ == "__main__":
    t = TestClass()
    device.start()
