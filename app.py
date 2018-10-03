from controller.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A', 'B')
def key_push(value):
    print(f"key_push value: {value}")


@device.listen('LEFT_STICK')
def stick_movement(value):
    print(f"stick_movement value: {value}")


if __name__ == "__main__":
    device.start()
