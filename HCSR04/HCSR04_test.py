############
# HCSR04_test.py test/demo of the HCSR04 module
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2019-08-28
# This software is licensed under the Eclipse Public License 2.0
############
from HCSR04 import HCSR04
import pyb

def main() :
  telemeter = HCSR04('X11', 'X12')
  
  while True :
    print('D:', telemeter.measure(), 'cm')
    pyb.delay(500)

def main_tmp() :
  from TMP36 import TMP36
  
  tmp = TMP36('Y12')
  telemeter = HCSR04('X11', 'X12', tmp36 = tmp)
  
  while True :
    print('D:', telemeter.measure(), 'cm')
    print('T:', tmp.measure()/10, '°C')
    pyb.delay(500)

def main_bme() :
  from BME280 import BME280
  
  bme = BME280(1)
  bme.normalmode()
  telemeter = HCSR04('X11', 'X12', bme280 = bme)
  
  while True :
    print('D:', telemeter.measure(), 'cm')
    print('T:', bme.measure()['temp']/100, '°C')
    pyb.delay(500)

# Try one of these according to the temperature sensor you have
main()
#main_bme()
#main_tmp()
