import usbtmc


def list_devices():
    """List all usbtmc compatible devices connected to PC."""
    if not usbtmc.list_resources():
        print("No device found.")
    else:
        for i in usbtmc.list_resources():
            inst = usbtmc.Instrument(i)
            print(inst.ask("*IDN?"))


def get_instrument(pos):
    """Returns a new instrument.

	Args:
	pos -- device position in devices list (provided by list_devices())
	"""
    return usbtmc.Instrument(usbtmc.list_resources()[pos])
