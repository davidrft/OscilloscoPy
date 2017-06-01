import usbtmc
import numpy as np
import matplotlib.pyplot as plt

def list_devices():
    if not usbtmc.list_resources():
        print("No device found.")
    else:
        for i in usbtmc.list_resources():
            inst = usbtmc.Instrument(i)
            print(inst.ask("*IDN?"))

class Osc(usbtmc.Instrument):
    
    def __init__(self, pos = 0):
        super(Osc, self).__init__(usbtmc.list_resources()[pos])
        
        
    def reset(self):
        self.write(":RST")
    
    
    def stop(self):
        self.write(":STOP")
    
    
    def run(self):
        self.write(":RUN")
    
    
    def single(self):
        self.write(":SINGLE")
        
        
    def get_time_scale(self):
        return float(self.ask(":TIM:SCAL?"))
        
        
    def get_time_pos(self):
       return float(self.ask(":TIM:POS?"))


    def get_volt_scale(self, channel):
        return float(self.ask(":CHAN{}:SCAL?".format(channel)))
    
    
    def get_volt_offset(self, channel):
        return float(self.ask(":CHAN{}:OFFS?".format(channel)))

    
    def set_scale(self, channel, scale):
        self.write(":CHAN{}:SCAL {}".format(channel, scale))

    
    def set_offset(self, channel, offset):
        self.write(":CHAN{}:OFFS {}".format(channel, offset))


    def gen_sin(self, amp, freq, offs=0):
        self.gen_on()
        self.write("WGEN:FUNC SIN;FREQ {};VOLT {};VOLT:OFFS {}".format(freq, amp, offs))


    def gen_sqr(self, amp, freq, duty_cicle=50, offs=0):
        self.gen_on()
        self.write("WGEN:FUNC SQU;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:SQU:DCYC {}".format(freq, amp, offs, duty_cicle))
    
    
    def gen_ramp(self, amp, freq, symmetry=50, offs=0):
        self.gen_on()
        self.write("WGEN:FUNC RAMP;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:RAMP:SYMM {}".format(freq, amp, offs, symmetry))
    
    
    def gen_pulse(self, amp, freq, width, offs=0):
        self.gen_on()
        self.write("WGEN:FUNC PULS;FREQ {};VOLT:HIGH {};VOLT:LOW {};:WGEN:FUNC:PULS:WIDT {}".format(freq, amp, offs, width))


    def gen_dc(self, amp):
        self.gen_on()
        self.write("WGEN:FUNC DC;VOLT:OFFS {}".format(amp))
    
    
    def gen_noise(self, amp, offs=0):
        self.write("WGEN:FUNC NOIS;VOLT {};VOLT:OFFS {}".format(amp, offs))
        self.write("WGEN:FUNC NOIS;VOLT {};VOLT:OFFS {}".format(amp, offs))
    
    
    def gen_on(self):
        self.write("WGEN:OUTP ON")
    
    
    def gen_off(self):
        self.write("WGEN:OUTP OFF")
                
                
    def toggle_channel(self, channel):
        status = self.ask("CHAN" + str(channel) + ":DISP?") == "1"
        if status:
            self.write("CHAN" + str(channel) + ":DISP OFF")
        else:
            self.write("CHAN" + str(channel) + ":DISP ON")
    
    
    def get_data(self, channel):
        self.stop()
        self.write(":SYST:HEAD OFF")
        self.write(":WAVEFORM:SOURCE CHAN" + str(channel))
        self.write(":WAVEFORM:POIN:MODE MAX")
        self.write(":WAVEFORM:FORMAT BYTE")
        
        self.write(":WAV:DATA?")
        rawdata = self.read_raw()
        data = np.frombuffer(rawdata, 'B')
        
        yorigin = float(self.ask(":WAV:YOR?"))
        yref = float(self.ask(":WAV:YREF?"))
        yinc = float(self.ask(":WAV:YINC?"))
        
        data = ((data - yref) * yinc) + yorigin 
        
        self.run()
        return data
        
        
    def show_img(self, channel=1):
        data = self.get_data(channel)
        
        timescale = float(self.ask(":TIM:SCAL?"))
                          
        time = np.linspace(-5*timescale, 5*timescale, len(data))
        
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
        plt.title("Oscilloscope Channel " + str(channel))
        plt.ylabel("Voltage (V)")
        plt.xlabel("Time ({})".format(t_unit))
        plt.xlim(time[0], time[-1])
        plt.ylim(-4*voltscale, 4*voltscale)
        plt.show()

x = Osc()

