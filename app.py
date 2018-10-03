import keyboard as keybard

from controller.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A', 'B')
def kage():
    print("KAGE!")
    return


if __name__ == "__main__":
    device.start()

    while True:
        if keybard.is_pressed('Esc'):
            print("WE ARE EXITING NOW!")
            device.term()
            exit(0)
