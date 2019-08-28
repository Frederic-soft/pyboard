############
# LEDMatrixExample.py  Example/demo of the LEDMatrixWithMax module
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2019-08-28
# This software is licensed under the Eclipse Public License 2.0
############
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
for _ in range(500) :
  m.setIntensity(intensity)
  pyb.delay(10)
  intensity += step
  if intensity == 0:
    step = 1
  if intensity == 100:
    step = -1

while True :
  for k in range(8) :
    m.clearDisplay()
    for i in range(k+1) :
      m.setPixel(i, k-i, True)
    m.updateDisplay()
    pyb.delay(100)
  for k in range(7) :
    m.clearDisplay()
    for i in range(k,7) :
      m.setPixel(7+k-i, i+1, True)
    m.updateDisplay()
    pyb.delay(100)
