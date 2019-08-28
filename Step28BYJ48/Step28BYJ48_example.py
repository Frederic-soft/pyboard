############
# Step28BYJ48_example.py  example of use of the Step28BYJ48 module
#
# Connect IN1..IN4 to pins X1..X4
# Connect the "-" pin to the GND pin of the pyboard
# Connect the "+" pin to the VIN pin of the pyboard
# Put the jumper on (connect the two pins on the right of the "-" and "+" pins)
#
# © Frédéric Boulanger <frederic.softdev@gmail.com>
# 2016-07-20
# This software is licensed under the Eclipse Public License 2.0
############
"""
"""
import Step28BYJ48
import pyb

stepper=Step28BYJ48.Step28BYJ48(pyb.Pin("X1"), pyb.Pin("X2"), pyb.Pin("X3"), pyb.Pin("X4"))
stepper.setSpeed(8192)

print("Forward")
stepper.syncSteps(512)

pyb.delay(1000)

print("Backward")
stepper.syncSteps(-512)

print("Forward async")
stepper.asyncSteps(512, callback=lambda t: print('Done'))

# Wait so that the callback prints its message before the program terminates
print("Waiting for stepper to finish")
pyb.delay(10000)

print("Bye!")
