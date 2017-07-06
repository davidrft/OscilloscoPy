import usbtmc
import numpy as np
import matplotlib.pyplot as plt


def list_devices():
    """List all usbtmc compatible devices connected to PC."""
    if not usbtmc.list_resources():
        print("No device found.")
    else:
        for i in usbtmc.list_resources():
            inst = usbtmc.Instrument(i)
            print(inst.ask("*IDN?"))


def instrument(pos):
	"""Returns a new instrument.

	Args:
	pos -- device position in devices list (provided by list_devices())
	"""
	return usbtmc.Instrument(usbtmc.list_resources()[pos])


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
        self.inst.write("WGEN:FUNC SIN;FREQ {};VOLT {};VOLT:OFFS {}"
                   .format(freq, amp, offs))

    def sqr(self, amp, freq, duty_cicle=50.0, offs=0.0):
        """Generates a square wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        duty_cycle -- wave duty_cicle in % (default 50.0)
        offs -- wave offset (default 0.0)
        """
        self.on()
        self.inst.write("WGEN:FUNC SQU;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:SQU:DCYC {}"
                   .format(freq, amp, offs, duty_cicle))
        
    def ramp(self, amp, freq, symmetry=50.0, offs=0.0):
        """Generates a ramp wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        duty_cycle -- wave symmetry in % (default 50.0)
        offs -- wave offset (default 0.0)
        """
        self.on()
        self.inst.write("WGEN:FUNC RAMP;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:RAMP:SYMM {}"
                   .format(freq, amp, offs, symmetry))
    
    def pulse(self, amp, freq, width, offs=0.0):
        """Generates a pulse wave.

        Args:
        amp -- wave amplitude
        freq -- wave frequency
        width -- pulse width
        offs -- wave offset (default 0.0)
        """
        self.on()
        self.inst.write("WGEN:FUNC PULS;FREQ {};VOLT:HIGH {};VOLT:LOW {};:WGEN:FUNC:PULS:WIDT {}"
                   .format(freq, amp, offs, width))

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


class Channels:
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
        return float(self.inst.ask("MEAS:PHAS? CHAN{},CHAN{}"
                                   .format(sel_channel, ref_channel)))
        
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
        data = np.frombuffer(rawdata[10:-1], 'B')
        
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


class Oscilloscope():    
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

