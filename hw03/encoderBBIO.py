#!/usr/bin/env python3
# From: https://adafruit-beaglebone-io-python.readthedocs.io/en/latest/Encoder.html
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP1, eQEP2
import time

# Instantiate the class to access channel eQEP2, and initialize
# that channel

myEncoder1 = RotaryEncoder(eQEP1)
myEncoder1.setAbsolute()
myEncoder1.enable()

myEncoder2 = RotaryEncoder(eQEP2)
myEncoder2.setAbsolute()
myEncoder2.enable()

print('frequency ' + str(myEncoder1.frequency))

# Get the current position
for i in range(1,50):
    print(myEncoder1.position)
    print(myEncoder2.position)
    time.sleep(0.1)
    
# cur_position = myEncoder1.position
# print(cur_position)

# # Set the current position
# next_position = 15
# myEncoder.position = next_position

# # Reset position to 0
# myEncoder.zero()

# # Change mode to relative (default is absolute)
# # You can use setAbsolute() to change back to absolute
# # Absolute: the position starts at zero and is incremented or
# #           decremented by the encoder's movement
# # Relative: the position is reset when the unit timer overflows.
# myEncoder.setRelative()

# # Read the current mode (0: absolute, 1: relative)
# # Mode can also be set as a property
# mode = myEncoder.mode

# # Get the current frequency of update in Hz
# freq = myEncoder.frequency

# # Set the update frequency to 1 kHz
# myEncoder.frequency = 1000

# # Disable the eQEP channel
# myEncoder.disable()

# # Check if the channel is enabled
# # The 'enabled' property is read-only
# # Use the enable() and disable() methods to
# # safely enable or disable the module
# isEnabled = myEncoder.enabled
