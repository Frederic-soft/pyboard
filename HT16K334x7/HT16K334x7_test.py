############
# HT16K334x7_test.py
# Test/demo file for the HT16K334x7 module
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2015-08-27
# This software is licensed under the Eclipse Public License 2.0
############
from HT16K334x7 import HT16K334x7

def main() :
	disp = HT16K334x7() # HT16K334x7 at address 0x70 on I2C bus 1
	disp.on()

	disp.displayNumber(1234)
	pyb.delay(1000)

	disp.displayString('cool')

	disp.set_brightness(15)
	for level in range(15,-1,-1):
		disp.set_brightness(level)
		pyb.delay(200)

	for level in range(15):
		disp.set_brightness(level)
		pyb.delay(200)
	disp.clear()

	snake = (
		0b00000001,
		0b10000010,
		0b01000000,
		0b10010000,
		0b00001000,
		0b10000100,
		0b01000000,
		0b10100000
	)
	sl = len(snake)
	for i in range(100):
		for d in range(4):
			disp.display(d, snake[(i + d) % sl])
		pyb.delay(50)
	disp.clear()

	disp.displayDigit(0,4)
	pyb.delay(500)
	disp.displayDigit(1,3)
	pyb.delay(500)
	disp.displayDigit(2,2)
	pyb.delay(500)
	disp.displayDigit(3,1)
	pyb.delay(500)

	for i in range(10000):
		disp.displayNumber(i)
		pyb.delay(3)

	disp.setDots(True)

	for i in range(4):
		disp.display(i, 0xFF)

	disp.blink(HT16K334x7.blink2Hz)
	pyb.delay(2000)

	disp.displayString('mPython = cool StuFF')

	disp.blink(HT16K334x7.blinkOff)

main()
