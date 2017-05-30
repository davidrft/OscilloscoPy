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
        
#    def get_time_offset(self):
#       return float(self.ask(":TIM:OFFS?"))


    def get_volt_scale(self, channel):
        return float(self.ask(":CHAN{}:SCAL?".format(channel)))
    
    
    def get_volt_offset(self, channel):
        return float(self.ask(":CHAN{}:OFFS?".format(channel)))

    
#    def set_scale(self, channel, scale):
#        self.write(":CHAN{}:SCAL{}".format(channel, scale))

    
#    def set_offset(self, channel, offset):
#        self.write(":CHAN{}:OFFS{}".format(channel, offset))


    def gen_sin(self, freq, amp, offs=0):
        self.write("WGEN:FUNC SIN;FREQ {};VOLT {};VOLT:OFFS {}".format(freq, amp, offs))


    def gen_sqr(self, amp, freq, duty_cicle=50, offs=0):
        self.write("WGEN:FUNC SQU;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:SQU:DCYC {}".format(freq, amp, offs, duty_cicle))
    
    
    def gen_ramp(self, amp, freq, symmetry=50, offs=0):
        self.write("WGEN:FUNC RAMP;FREQ {};VOLT {};VOLT:OFFS {};:WGEN:FUNC:RAMP:SYMM {}".format(freq, amp, offs, symmetry))
    
    
    def gen_pulse(self, amp, freq, width, offs=0):
        self.write("WGEN:FUNC PULS;FREQ {};VOLT:HIGH {};VOLT:LOW {};:WGEN:FUNC:PULS:WIDT {}".format(freq, amp, offs, width))


    def gen_dc(self, amp):
        self.write("WGEN:FUNC DC;VOLT:OFFS {}".format(amp))
    
    
    def gen_noise(self, amp, offs=0):
        self.write("WGEN:FUNC NOIS;VOLT {};VOLT:OFFS {}".format(amp, offs))
    
    
    def toggle_channel(self, channel):
        status = self.ask("CHAN" + str(channel) + ":DISP?") == "1"
        if status:
            self.write("CHAN" + str(channel) + ":DISP OFF")
        else:
            self.write("CHAN" + str(channel) + ":DISP ON")
    
#    def save_img(self):
        #self.stop()
        #self.write(":SYST:HEAD OFF")
        #self.write(":WAV:SOUR CHAN1")
        #self.write(":WAV:POIN:MODE NORM")
        
        #self.write(":WAV:DATA?")
        #rawdata = self.read_raw(9000)
        #data = np.frombuffer(rawdata, 'B')
        
        #voltscale = float(self.ask(":CHAN1:SCAL?"))
        #voltoffs = float(self.ask(":CHAN1:OFFS?"))
        
        #data = data * -1 + 255
        #data = (data - 130.0 - voltoffs/voltscale*25) / 25 * voltscale
        
        #print(data)
        #print("Tamanho data: " + str(data.size))
        
        #timescale = float(self.ask(":TIM:SCAL?"))
                          
        #time = np.linspace(-5*timescale, 5*timescale, 9000)
        #print(time)
        #print("Tamanho time: " + str(time.size))
        
        
        #if (time[8999] < 1e-3):
            #time = time * 1e6
            #t_unit = "uS"
        #elif (time[8999] < 1):
            #time = time * 1e3
            #t_unit = "mS"
        #else:
            #t_unit = "S"
        
        #self.run()
        
        #plt.plot(time, data)
        #plt.title("Oscilloscope Channel 1")
        #plt.ylabel("Voltage (V)")
        #plt.xlabel("Time ({})".format(t_unit))
        #plt.xlim(time[0], time[8999])
        #plt.show()

x = Osc()

