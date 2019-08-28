############
# LEDMatrixWithMAX.py  a Micropython pyboard driver for an 8x8 LED matrix
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2015-06-16
# This software is licensed under the Eclipse Public License 2.0
############
from MAX7219 import *

""" Test program
import pyb
from LEDMatrixWithMAX import *

m = LEDMatrixWithMAX(1)
m.on()
m.clearDisplay()
for i in range(8):
    m.setPixel(i,i,True)
m.updateDisplay()

intensity = 100
step = -1
while True:
	m.setIntensity(intensity)
	pyb.delay(10)
	intensity += step
	if intensity == 0:
		step = 1
	if intensity == 100:
		step = -1
"""

class LEDMatrixWithMAX:
	def __init__(self, bus):
		"""
		Create a new LED matrix
		
		When bus = 1, CLK = X6, CS = X5, DIN = X8
		When bus = 2, CLK = Y6, CS = Y5, DIN = Y8
		"""
		self.max = MAX7219(bus)
		self.max.scan(8)
		self.max.decode(MAX7219.NO_DECODE)
		self.max.test(MAX7219.NOTEST)
		self.bitmap = bytearray(8)
		self.clearDisplay()
	
	def on(self, on=True):
		""" Turn the matrix on or off """
		if on:
			self.max.switch(MAX7219.ON)
		else:
			self.max.switch(MAX7219.OFF)
	
	def clearBitmap(self):
		""" Set all pixels off (does not change the LEDs) """
		for i in range(8):
			self.bitmap[i] = 0
	
	def updateDisplay(self):
		""" Refresh the LEDs so that they match the pixels """
		for i in range(8):
			self.max.digit(i, self.bitmap[i])
	
	def clearDisplay(self):
		""" Set all pixels and LEDs off """
		self.clearBitmap()
		self.updateDisplay()
	
	def setPixel(self, x, y, on):
		""" Switch a given pixel on or off (does not change the LED) """
		if on:
			self.bitmap[x] |= 2**y
		else:
			self.bitmap[x] &= ~(2**y)

	def setIntensity(self, percent):
		""" Set the light intensity of the LEDs """
		self.max.intensity(percent)
	
	def showImage(self, image):
		"""
		Display an image on the LED matrix.
		
		The image should be a list or tuple of 8 lists or tuples or integers or strings.
		If the elements are lists or tuples, they should contains 8 values which will 
			be interpreted as booleans to switch the LEDs on or off.
		If the elements are integers, their 8 least significant bits will be used 
			to drive the LEDs on or off.
		If the elements are strings, they must have 8 characters.
			Spaces are interpreted as off, other characters are interpreted as on.
		"""
		if not isinstance(image, (list, tuple)):
			raise RuntimeError("Image is not a list")
		if len(image) != 8:
			raise RuntimeError("Image does not have 8 components")
		if isinstance(image[0], int):
			for i in range(8):
				value = image[i]
				for j in range(8):
					self.setPixel(j, i, value & 2**(7 - j))
		elif isinstance(image[0], str):
			for i in range(8):
				if len(image[i]) != 8:
					raise RuntimeError("String in image does not have 8 character")
				for j in range(8):
					self.setPixel(j, i, image[i][j] != ' ')
		elif isinstance(image[0], (tuple, list)):
			for i in range(8):
				if len(image[i]) != 8:
					raise RuntimeError("List in image does not have 8 items")
				for j in range(8):
					self.setPixel(j, i, image[i][j])
		else:
			raise RuntimeError("Could not interpret image")
		self.updateDisplay()
