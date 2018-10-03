"""Simple example showing how to get gamepad events."""
import keyboard as keyboard

from controller.Controller import Controller

c = Controller()

if __name__ == "__main__":
    c.start()

    while True:
        if keyboard.is_pressed('Esc'):
            print("WE ARE EXITING NOW!")
            c.term()
            exit(0)
