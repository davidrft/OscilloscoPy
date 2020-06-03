class Oscilloscope:
    def __init__(self, inst):
        """Initializes a new device.

        Args:
        inst -- instrument in which the oscilloscope is
        """
        self.inst = inst

    def reset(self):
        """Resets device."""
        self.inst.write(":RST")

    def stop(self):
        """Stops acquisition and shows the last capture."""
        self.inst.write(":STOP")

    def run(self):
        """Resumes device."""
        self.inst.write(":RUN")

    def single(self):
        """Acquire a single waveform and then stops."""
        self.inst.write(":SINGLE")

    def auto_scale(self):
        """Auto scale active channels."""
        self.inst.write(":AUT")

    def set_acquire(self, mode):
        """Set the waveform acquire mode.

        Args:
        mode -- 'normal', 'average', 'hres' or 'peak'
        """
        self.inst.write(":ACQ:TYPE {}".format(mode.upper()))
