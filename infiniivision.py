import pyoscilloscope as posc
import usbtmc

class Infiniivision:
    def __init__(self, pos = 0):
        self.inst = posc.instrument(pos)
        self.gen = posc.Generator(self.inst)
        self.chan = posc.Channels(self.inst)
        self.osc = posc.Oscilloscope(self.inst)
    
    def show_img(self, channel=1):
        """Prints acquired waveform from selected channel on PC.

        Args:
        channel -- selected channel (default 1)
        """
        self.stop()
        time, data = self.get_data(channel)
        self.run()
        
        if (time[-1] < 1e-3):
            time = time * 1e6
            t_unit = "uS"
        elif (time[-1] < 1):
            time = time * 1e3
            t_unit = "mS"
        else:
            t_unit = "S"
        
        voltscale = self.get_volt_scale(channel)
        voltoffs = self.get_volt_offset(channel)
        
        plt.plot(time, data)
        plt.title("Oscilloscope Channel {}".format(channel))
        plt.ylabel("Voltage (V)")
        plt.xlabel("Time ({})".format(t_unit))
        plt.xlim(time[0], time[-1])
        plt.ylim(-4*voltscale, 4*voltscale)
        plt.show()