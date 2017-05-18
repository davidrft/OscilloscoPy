import usbtmc

def list_devices():
    if not usbtmc.list_resources():
        print("No device found.")
    else:
        for i in usbtmc.list_resources():
            inst = usbtmc.Instrument(i)
            print(inst.ask("*IDN?"))

class Oscilloscope(usbtmc.Instrument):
    
    inst = None

    def __init__(self, pos):
        self.__super__(usbtmc.list_resources()[pos])


def main():
    list_devices()

if __name__ == "__main__":
    main()
