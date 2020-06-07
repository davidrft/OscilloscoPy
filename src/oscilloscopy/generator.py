class Generator:
    def __init__(self, inst):
        """Initializes a new device.

        Args:
        inst -- instrument in which the generator is
        """
        self.inst = inst
        self.inst.write(":WAV:FORM BYTE")
        self.inst.write(":WAV:POIN:MODE MAX")

    def sin(self, amp, freq, offs=0.0):
        """Generates a sinoidal wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        offs -- wave offset (default 0.0)
        """
        self.on()
        self.inst.write(
            "WGEN:FUNC SIN;FREQ {};VOLT {};VOLT:OFFS {}".format(freq, amp, offs)
        )

    def square(self, amp, freq, duty_cycle=50.0, offs=0.0):
        """Generates a square wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        duty_cycle -- wave duty_cycle in % (default 50.0)
        offs -- wave offset (default 0.0)
        """
        self.on()
        self.inst.write(
            "WGEN:FUNC SQU;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:SQU:DCYC {}".format(
                freq, amp, offs, duty_cycle
            )
        )

    def ramp(self, amp, freq, symmetry=50.0, offs=0.0):
        """Generates a ramp wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        duty_cycle -- wave symmetry in % (default 50.0)
        offs -- wave offset (default 0.0)
        """
        self.on()
        self.inst.write(
            "WGEN:FUNC RAMP;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:RAMP:SYMM {}".format(
                freq, amp, offs, symmetry
            )
        )

    def pulse(self, amp, freq, width, offs=0.0):
        """Generates a pulse wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        width -- pulse width
        offs -- wave offset (default 0.0)
        """
        self.on()
        self.inst.write(
            "WGEN:FUNC PULS;FREQ {};VOLT:HIGH {};VOLT:LOW {};:WGEN:FUNC:PULS:WIDT {}".format(
                freq, amp, offs, width
            )
        )

    def dc(self, amp):
        """Generates a DC voltage.

        Args:
        amp -- wave amplitude
        """
        self.on()
        self.inst.write("WGEN:FUNC DC;VOLT:OFFS {}".format(amp))

    def noise(self, amp, offs=0.0):
        """Generates noise.

        Args:
        amp -- noise amplitude
        offs -- noise offset (default 0.0)
        """
        self.inst.write("WGEN:FUNC NOIS;VOLT {};VOLT:OFFS {}".format(amp, offs))

    def on(self):
        """Turns Wave Generator on."""
        self.inst.write("WGEN:OUTP ON")

    def off(self):
        """Turns Wave Generator off."""
        self.inst.write("WGEN:OUTP OFF")
