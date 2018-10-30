from inputz.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A', 'B')
def key_push(value):
    print(f"key_push value 2: {value}")


@device.listen('A')
def push_a(value):
    if value:
        device.vibrate([1, 1])

    print(f"push_a: {value}")


@device.listen('B')
def push_b(value):
    if value:
        device.vibrate([0, 0])
    print(f"push_b: {value}")


@device.listen('RIGHT_BUMPER')
def right_bumper(value):
    print(f"right_bumpervalue: {value}")


@device.listen('LEFT_BUMPER')
def left_bumper(value):
    print(f"left_bumpervalue: {value}")


@device.listen('RIGHT_STICK')
def right_stick(value):
    # device.vibrate(value)
    print(f"right_stick: {value}")


@device.listen('LEFT_STICK')
def left_stick(value):
    # device.vibrate(value)
    print(f"left_stick: {value}")


if __name__ == "__main__":
    device.run_unsecure()
    device.start()
