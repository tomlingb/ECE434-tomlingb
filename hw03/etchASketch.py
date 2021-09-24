#!/usr/bin/env python3
import curses
from curses import wrapper
import smbus
import time
import numpy
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP1, eQEP2


bus = smbus.SMBus(2)  # Use i2c bus 2
matrix = 0x70         # Use address 0x70

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

matrixData = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

tracker = numpy.zeros((64,), dtype=int)

head = 27
tracker[head] = 1

myEncoder1 = RotaryEncoder(eQEP1)
myEncoder1.setAbsolute()
myEncoder1.enable()

myEncoder2 = RotaryEncoder(eQEP2)
myEncoder2.setAbsolute()
myEncoder2.enable()

rightValue = myEncoder2.position
leftValue = myEncoder1.position

#actual game logic
while True:
    dirCount = 0
    if(myEncoder2.position >= rightValue + 2):
        direction = "Left"
    elif(myEncoder2.position <= rightValue - 2):
        direction = "Right"
    else:
        dirCount += 1
    rightValue = myEncoder2.position
    if(myEncoder1.position >= leftValue + 2):
        direction = "Up"
    elif(myEncoder1.position <= leftValue - 2):
        direction = "Down"
    else:
        dirCount += 1
    leftValue = myEncoder1.position
    
    if(dirCount == 2):
        direction = "None"
        
    if(direction=="Up"): 
        if(head % 8 != 7): #checks the border of the window so you cant draw past it
            head+=1
            tracker[head] = 1
    elif(direction=="Left"):
        if(head-8 > -1 ):
            head-=8
            tracker[head] = 1
    elif(direction=="Down"):
        if(head % 8 != 0):
            head-=1
            tracker[head] = 1
    elif(direction=="Right"):
        if(head+8 < 64):
            head+=8
            tracker[head] = 1

    for i in range(8):
        count = 0
        for j in range(8):
            if tracker[(i)*8 + (j)] == 1:
                count = count + 2 ** j
        matrixData[i*2 + 1] = count
        
    for i in range(8):
        matrixData[i*2] = 0
    matrixData[int(head/8)*2] = 2**(head%8)
    bus.write_i2c_block_data(matrix, 0, matrixData)