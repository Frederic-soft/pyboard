############
# SpiritLevel.py
#
# This code uses the built-in MMA7660 accelerometer of the pyboard and
# an attached 8x8 LED matrix driven by a MAX7219 to build a spirit level.
# Everything is handled using interrupts.
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2015-06-16
# This software is licensed under the Eclipse Public License 2.0
############
# Import the MMA7660 driver
from MMA7660 import *
# Import the LED matrix driver
from LEDMatrixWithMAX import *

mma = MMA7660()             # our accelerometer
led = LEDMatrixWithMAX(1)   # the LED matrix, connected on SPI bus 2
# Y5 = NSS (CS), Y6 = SCK (CLK), (Y7 = MISO, not used) and Y8 = MOSI (DIN)

accel = bytearray(3)        # buffer for reading data samples from the accelerometer

# Buffer for the window avarage
wsize = 16          # width of the window
xbuf = [0] * wsize  # buffer for x acceleration
ybuf = [0] * wsize  # buffer for y acceleration
idx = 0             # current index for writing into the buffer

"""
Compute the integer mean of a buffer
"""
def mean(buf):
	m = 0
	for i in range(len(buf)):  # cannot use "for x in buf" in an interrupt handler
		m += buf[i]
	return m // len(buf)

"""
Read the accelerometer data, update the average window,
and move the bubble on the LED matrix accordingly.
"""
def moveBubble(line):
	global idx
	
	mma.getSample(accel)      # get a sample of data from the accelerometer
	x = accel[0]              # acceleration along the x axis
	if x > 31:                # interpret as 2's complement
		x -= 64
	xbuf[idx] = x             # update window average buffer
	y = accel[1]              # same processing for y axis acceleration
	if y > 31:
		y -= 64
	ybuf[idx] = y
	idx = (idx + 1) % wsize   # advance buffer index
	x = mean(xbuf) + 1        # get the mean x axis average over the window
	y = mean(ybuf) + 1        # get the mean y axis average over the window
	x = (6 * x) // 32         # scale the value from -32/31 to -6/+5
	x += 3                    # center of the matrix is (3,3)
	if x < 0: x = 0           # avoid indexing out of range
	if x > 6: x = 6
	x = 6 - x                 # reverse x axis display
	y = (6 * y) // 32         # same processing for the y axis
	y += 3
	if y < 0: y = 0
	if y > 6 : y = 6
	led.clearBitmap()         # clear the LED matrix
	led.setPixel(x, y, True)  # switch on 4 LEDs (the bubble) on the matrix
	led.setPixel(x+1, y, True)
	led.setPixel(x, y+1, True)
	led.setPixel(x+1, y+1, True)
	led.updateDisplay()       # update the display

# Get 16 samples per second
mma.setActiveSamplingRate(MMA7660.AM16)
# Install the moveBubble function as interrupt handler
mma.setInterruptHandler(moveBubble)
# Enable interrupts when the accelerometer data is refreshed
mma.enableInterrupt(MMA7660.GINT)
# Switch the accelerometer to active mode
mma.on(True)
# Switch the LED matrix on
led.on(True)
##########################################################################
