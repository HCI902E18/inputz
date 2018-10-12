from inputz.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A')
def test_func(args):
    print('test_func', args)
    return


if __name__ == "__main__":
    test_func("1")
    test_func("2")
    test_func("3")
    test_func("4")
    test_func("5")
    test_func("6")
    device.start()
