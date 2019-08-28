############
# HCSR04.py a Micropython pyboard driver for the HCSR04 ultrasound telemeter.
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2019-08-28
# This software is licensed under the Eclipse Public License 2.0
############
import pyb

class HCSR04:
	"""
	Measure a distance using an HC-SR04 ultrasonic ranging module
	
	Example: usrange = HCSR04('X11', 'X12')
	With temperature correction:
	tmp36 = TMP36('X19')
	usrange = HCSR04('X11', 'X12', tmp36)
	"""
	speed15 = 340    # 340m/s at 15°C
	refTemp = 15     # reference temperature in Celsius
	corr = 0.607     # +0.607m/s / °C
	
	
	def __init__(self, trig, echo, tmp36 = None, bme280 = None):
		"""
		Initialize an HCSR04 with the trigger input on pin with name trig 
		and the echo output on pin with name echo.
		The optional tmp36 is an instance of TMP36 to measure the temperature 
		in order to adjust the speed of sound.
		The optional bme280 is an instance of BME280 to measure the temperature 
		in order to adjust the speed of sound.
		"""
		self.trig = pyb.Pin(trig, pyb.Pin.OUT_PP)
		self.echo = pyb.Pin(echo, pyb.Pin.IN, pyb.Pin.PULL_NONE)
		self.tmp36 = tmp36
		self.bme280 = bme280

	def measure(self):
		"""
		Perform one measure of distance, with result in centimeters.
		"""
		self.trig.value(0)
		pyb.delay(1)
		self.trig.value(1)
		pyb.udelay(11)
		self.trig.value(0)
		while self.echo.value() == 0 :
			pass
		start = pyb.micros()
		while self.echo.value() == 1 :
			pass
		elapsed = pyb.elapsed_micros(start)
		speed = HCSR04.speed15
		temp = HCSR04.refTemp
		if self.tmp36 != None :
			temp = self.tmp36.temp() / 10
		if self.bme280 != None :
			temp = self.bme280.measure()['temp'] / 100
		speed += (temp - HCSR04.refTemp) * HCSR04.corr
		# speed m/s * elapsed E-6 s / 2 = 170 E -6 m = 170 E -4 cm
		return (speed * elapsed) * 0.5E-4
	
	def distance(self):
		"""
		Return the average of a series of 5 measures, in centimeters.
		"""
		d = 0
		for i in range(5) :
			d += self.measure()
			pyb.delay(1)
		return d / 5
	
	def unlock(self):
		"""
		Unlock the device if it always returns null distances.
		Forces the 'echo' output to 0 during 100ms to unlock the module.
		"""
		self.echo.init(pyb.Pin.OUT_PP)
		self.echo.value(0)
		pyb.delay(100)
		self.echo.init(pyb.Pin.IN, pyb.Pin.PULL_NONE)
