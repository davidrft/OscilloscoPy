import pyoscilloscope as posc
import usbtmc

class Infiniivision:
	def __init__(self, pos = 0):
		self.inst = posc.instrument(pos)
		self.gen = posc.Generator(self.inst)
		self.chan = posc.Channels(self.inst)
		self.osc = posc.Oscilloscope(self.inst)
