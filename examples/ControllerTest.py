from inputz import Input
from inputz.Devices import Devices


class ControllerTest(object):
    def __init__(self):
        d = Devices()

        self.device = d.get_device()

        self.keys = [k for k, v in self.device.__dict__.items() if isinstance(v, Input)]

        self.pop_next()

        self.device.run_unsecure()
        self.device.start()

    def pop_next(self):
        if len(self.keys) > 0:
            key = self.keys.pop()
            self.device.clear_invocations()

            print(f"Press {key}")
            self.device.method_listener(self.key, key)
        else:
            print("ALL KEYS SUCCESSFULLY FOUND!")
            self.device.terminate()
            exit(1)

    def key(self, val):
        print('PRESSED')
        self.pop_next()


if __name__ == "__main__":
    ct = ControllerTest()
