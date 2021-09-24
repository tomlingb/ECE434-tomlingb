#!/usr/bin/env python3

import smbus
import time

bus = smbus.SMBus(2)
address1 = 0x4a
address2 = 0x48

while True:
    temp1 = bus.read_byte_data(address1, 0)
    temp2 = bus.read_byte_data(address2, 0)
    print("Temp1: {}     Temp2: {}".format(temp1, temp2), end = "\r")
    time.sleep(0.25)

