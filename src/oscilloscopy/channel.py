import numpy as np


class Channel:
    def __init__(self, inst):
        """Initializes a new device.

        Args:
        inst -- instrument in which the channels are
        """
        self.inst = inst
        self.inst.write(":WAV:FORM BYTE")
        self.inst.write(":WAV:POIN:MODE MAX")

    def get_time_scale(self):
        """Returns current time scale."""
        return float(self.inst.ask(":TIM:SCAL?"))

    def set_time_scale(self, scale):
        """Returns current time scale."""
        self.inst.write(":TIM:SCAL {}".format(scale))

    def get_time_delay(self):
        """Returns current time delay."""
        return float(self.inst.ask(":TIM:POS?"))

    def set_time_delay(self, delay):
        """Sets time delay to chosen value.
        
        Args:
        delay -- time delay to set
        """
        self.inst.write(":TIM:POS {}".format(delay))

    def get_volt_scale(self, channel):
        """Returns current voltage scale of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.inst.ask(":CHAN{}:SCAL?".format(channel)))

    def set_volt_scale(self, channel, scale):
        """Sets voltage scale of the selected channel to chosen value.

        Args:
        channel -- selected channel
        scale   -- voltage scale to set
        """
        self.inst.write(":CHAN{}:SCAL {}".format(channel, scale))

    def get_volt_offset(self, channel):
        """Returns current voltage offset of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.inst.ask(":CHAN{}:OFFS?".format(channel)))

    def set_volt_offset(self, channel, offset):
        """Sets voltage offset of the selected channel to chosen value.

        Args:
        channel -- selected channel
        offset  -- voltage offset to set
        """
        self.inst.write(":CHAN{}:OFFS {}".format(channel, offset))

    def auto_trigger(self, channel):
        """Set trigger level to 50% in selected channel.
        
        Args:
        channel -- selected channel
        """
        self.inst.write(":TRIG:SOUR CHAN{}".format(channel))
        self.inst.write(":TRIG:LEV:ASET")

    def set_trigger(self, channel, level=0):
        """Set trigger level to chosen value in selected channel.
        
        Args:
        channel -- selected channel
        level   -- trigger level to set in volts (default 0)
        """
        self.inst.write(":TRIG:SOUR CHAN{}".format(channel))
        self.inst.write(":TRIG:LEV {}".format(level))

    def get_vpp(self, channel):
        """Returns peak-to-peak measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.inst.ask(":MEAS:VPP? CHAN{}".format(channel)))

    def get_vrms(self, channel):
        """Returns rms measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.inst.ask(":MEAS:VRMS? CHAN{}".format(channel)))

    def get_frequency(self, channel):
        """Returns frequency measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.inst.ask(":MEAS:FREQ? CHAN{}".format(channel)))

    def get_period(self, channel):
        """Returns period measurement of the selected channel.

        Args:
        channel -- selected channel
        """
        return float(self.inst.ask(":MEAS:PER? CHAN{}".format(channel)))

    def get_phase(self, sel_channel, ref_channel):
        """Returns phase difference between selected and reference channel
        in degrees.

        Args:
        sel_channel -- selected channel
        ref_channel -- reference channel
        """
        return float(
            self.inst.ask("MEAS:PHAS? CHAN{},CHAN{}".format(sel_channel, ref_channel))
        )

    def set_coupling(self, channel, mode):
        """Sets coupling mode of the selected channel to chosen value.

        Args:
        channel -- selected channel
        mode    -- "AC" or "DC"
        """
        self.inst.write(":CHAN{}:COUP {}".format(channel, mode))

    def toggle_channel(self, channel):
        """Toggles selected channel status.

        Args:
        channel -- selected channel
        """
        status = self.inst.ask("CHAN{}:DISP?".format(channel)) == "1"
        if status:
            self.inst.write("CHAN{}:DISP OFF".format(channel))
        else:
            self.inst.write("CHAN{}:DISP ON".format(channel))

    def get_data(self, channel, points=1000):
        """Returns wave data from selected channel as a numpy array.

        Args:
        channel -- selected channel
        points  -- number of points to be acquired
        """
        self.inst.write(":DIG CHAN{}".format(channel))
        self.inst.write(":WAV:POIN {}".format(points))
        self.inst.write(":WAV:SOURCE CHAN{}".format(channel))
        self.inst.write(":WAV:DATA?")
        rawdata = self.inst.read_raw()
        data = np.frombuffer(rawdata[10:-1], "B")

        yorigin = float(self.inst.ask(":WAV:YOR?"))
        yref = float(self.inst.ask(":WAV:YREF?"))
        yinc = float(self.inst.ask(":WAV:YINC?"))

        xorigin = float(self.inst.ask(":WAV:XOR?"))
        xref = float(self.inst.ask(":WAV:XREF?"))
        xinc = float(self.inst.ask(":WAV:XINC?"))

        data_y = ((data - yref) * yinc) + yorigin
        data_x = np.array(range(len(data)))
        data_x = ((data_x - xref)) * xinc + xorigin

        return data_x, data_y
