from inputz.Devices import Devices

d = Devices()

device = d.get_device()


@device.listen('A')
def test_func(args):
    print('test_func', args)
    return


if __name__ == "__main__":
    test_func("kage")
    test_func("kage")
    test_func("kage")
    test_func("kage")
    test_func("kage")
    test_func("kage")
    device.start()
