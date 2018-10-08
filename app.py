from controller.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A', 'B')
def key_push(value):
    print(f"key_push value 2: {value}")


@device.listen('RIGHT_BUMPER')
def right_bumper(value):
    device.vibrate(value)
    print(f"right_bumpervalue: {value}")


if __name__ == "__main__":
    device.start()
