#!/usr/bin/env python3
import curses
from curses import wrapper
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP1, eQEP2
import Adafruit_BBIO.GPIO as GPIO
import smbus
import time
import numpy
import signal
import sys

#########################################
# Geoffrey Tomlinson                    #
# 9/24/2021                             #
# ECE434 HW03                           #
# Etch a sketch on a bicolor matrix     #
#########################################

#catches ctrl+C to suppress annoying output
def signal_handler(sig, frame):
    print('\rQuitting')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#startup message
print("Running Etch-A-Sketch")
print("Use the rotary encoders to control the cursor")
print("Press the top pushbutton to clear")
print("Press the bottom pushbutton to quit\n")

clearSW="P9_18"
quitSW="P9_17"
GPIO.setup(clearSW, GPIO.IN)
GPIO.setup(quitSW, GPIO.IN)

bus = smbus.SMBus(2)  # Use i2c bus 2
matrix = 0x70         # Use address 0x70

bus.write_byte_data(matrix, 0x21, 0)   # Start oscillator (p10)
bus.write_byte_data(matrix, 0x81, 0)   # Disp on, blink off (p11)
bus.write_byte_data(matrix, 0xe7, 0)   # Full brightness (page 15)

#create initial bicolor matrix data
matrixData = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]

#create 64 item arrray of zeros to track the location of the cursor
#tracker[0] being the bottom left corner and tracker[63] the top right
tracker = numpy.zeros((64,), dtype=int)


head = 27   #cursor location
tracker[head] = 1   #place a 1 in the tracker array to later be turned into a dot on the matrix

#setup the encoders
myEncoder1 = RotaryEncoder(eQEP1) #Up/Down encoder
myEncoder1.setAbsolute()
myEncoder1.enable()

myEncoder2 = RotaryEncoder(eQEP2) #Right/Left encoder
myEncoder2.setAbsolute()
myEncoder2.enable()

rightValue = myEncoder2.position #in reference to their position on my board
leftValue = myEncoder1.position #in reference to their position on my board

cleared = False #used to store if the screen is blank or not

#actual game logic
while True:
    dirCount = 0
    #checks if the cursor is being moved Right or Left
    if(myEncoder2.position >= rightValue + 2):
        direction = "Left"
    elif(myEncoder2.position <= rightValue - 2):
        direction = "Right"
    else:
        dirCount += 1
    rightValue = myEncoder2.position
    
    #checks if the cursor is being moved up or down
    if(myEncoder1.position >= leftValue + 2):
        direction = "Up"
    elif(myEncoder1.position <= leftValue - 2):
        direction = "Down"
    else:
        dirCount += 1
    leftValue = myEncoder1.position
    
    if(dirCount == 2): #if neither encoder is moved then do nothing
        direction = "None"
        
    if(direction=="Up"): 
        #cleared = False
        if(head % 8 != 7): #checks the border of the window so you cant draw past it
            head+=1
            tracker[head] = 1
    elif(direction=="Left"):
        #cleared = False
        if(head-8 > -1 ):
            head-=8
            tracker[head] = 1
    elif(direction=="Down"):
        #cleared = False
        if(head % 8 != 0):
            head-=1
            tracker[head] = 1
    elif(direction=="Right"):
        #cleared = False
        if(head+8 < 64):
            head+=8
            tracker[head] = 1
    if(GPIO.input(clearSW)):
        if(cleared == False): #output suppression
            cleared = True
        for i in range(64):
            tracker[i] = 0
            head = 27
            tracker[head] = 1
    if(GPIO.input(quitSW)):
        print("Quitting")
        break
    
    if(cleared):
        time.sleep(1)
        print("Clearing matrix")
        for fade in range(0xef, 0xe0, -1):
            bus.write_byte_data(matrix, fade, 0)
            time.sleep(0.1)  
        cleared = False
        bus.write_byte_data(matrix, 0xe7, 0)

    #draw the trace in red on the matrix
    for i in range(8): 
        count = 0
        for j in range(8):
            if tracker[(i)*8 + (j)] == 1 and i*8 + j != head: #makes sure not to draw red where the head is
                count = count + 2 ** j
        matrixData[i*2 + 1] = count
    
    #draw the head in green on the matrix
    for i in range(8):
        matrixData[i*2] = 0
    matrixData[int(head/8)*2] = 2**(head%8)
    bus.write_i2c_block_data(matrix, 0, matrixData)