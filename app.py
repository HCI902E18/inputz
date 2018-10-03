import keyboard as keybard

from controller.Devices import Devices


def main():
    d = Devices()

    device = d.get_device()

    return device


if __name__ == "__main__":
    k = main()

    while True:
        if keybard.is_pressed('Esc'):
            print("WE ARE EXITING NOW!")
            k.term()
            exit(0)
