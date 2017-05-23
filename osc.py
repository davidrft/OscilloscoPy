import usbtmc

def list_devices():
    if not usbtmc.list_resources():
        print("No device found.")
    else:
        for i in usbtmc.list_resources():
            inst = usbtmc.Instrument(i)
            print(inst.ask("*IDN?"))

class Osc(usbtmc.Instrument):
    
    inst = None

    def __init__(self, pos):
        super(Osc, self).__init__(usbtmc.list_resources()[pos])
        
        
    def reset(self):
        self.write("*RST")
        
        
    def get_time_scale(self):
        return float(self.ask(":TIM:SCAL?"))
        
        
    def get_time_offset(self):
        return float(self.ask(":TIM:OFFS?"))
        
        
    def get_volt_scale(self, channel):
        return float(self.ask(":CHAN" + str(channel) + ":SCAL?"))
    
    
    def get_volt_offset(self, channel):
        return float(self.ask(":CHAN" + str(channel) + ":OFFS?"))

    #def setScale(x):
        
def main():
    x = osc.Osc(0)

if __name__ == "__main__":
    main()
