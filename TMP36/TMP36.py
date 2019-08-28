############
# TMP36.py a Micropython pyboard driver for the TMP36 temperature sensor.
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2016-07-18
# This software is licensed under the Eclipse Public License 2.0
############
import pyb

class TMP36:
	"""
	A class to read the temperature using a TMP36 sensor.
	
	Bottom view of the TMP36 (pin side)
     _________
    | 1  2  3 |
    \         /
     ---------
     
    1 = Vs   2 = Out   3 = Gnd

    The output is 750mV at 25°C with 10mV/1°C
    The range is -40°C (100mV) to 125°C (1.75V)

	Example: temp = TMP36('X19')
	         print(temp.temp()
	"""
	offset = 750       # 750mV at 25°C
	refTemp = 25
	vRef = 3300        # input scale 0 - 3.3V
	resolution = 4096  # 16 bits
	
	def __init__(self, pinName):
		"""Initialize a sensor on pin with name pinName.
		   The pin must be able to perform ADC.
		"""
		self.pin = pyb.ADC(pyb.Pin(pinName))
	
	def measure(self):
		"""Perform one measure, the result is in tenth of °C to avoid using floats."""
		val = self.pin.read()
		volt = (val * TMP36.vRef) // TMP36.resolution
		return 10*TMP36.refTemp + (volt - TMP36.offset)

	def temp(self):
		"""Return the average of a series of measures, in tenth of °C."""
		temp = 0
		# Average of 10 measures
		for i in range(10):
			temp += self.measure()
			pyb.delay(5)
		return temp // 10
