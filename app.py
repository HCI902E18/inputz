from controller.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A', 'B')
def key_push(value):
    print(f"key_push value: {value}")
    device.kage(value)


@device.listen('RIGHT_STICK')
def bumber_movement(value):
    print(f"bumber_movement value: {value}")


if __name__ == "__main__":
    device.start()
