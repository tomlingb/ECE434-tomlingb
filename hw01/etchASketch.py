#!/usr/bin/env python3
import curses
from curses import wrapper


def main(stdscr):
    # Clear screen
    stdscr.clear()
    hwidth = int(stdscr.getmaxyx()[1]/2)
    message = "Etch-A-Sketch"
    printLocation = hwidth - int(len(message)/2)
    stdscr.addstr(0,printLocation,"{}\n\r".format(message))
    pos = (20,hwidth)
    stdscr.hline(1,0,"=",stdscr.getmaxyx()[1])
    stdscr.hline(stdscr.getmaxyx()[0] - 6,0,"=",stdscr.getmaxyx()[1])
    stdscr.addstr(stdscr.getmaxyx()[0] - 5,0,"Use WASD to control the Etch-A-Sketch\n\rPress C to clear the screen\n\rctrl+C to quit")
    stdscr.addstr(pos[0],pos[1],"")
    
    while True:
        stdscr.refresh()
        key = stdscr.getkey()
        
        if(key=="w"): 
            if(pos[0] - 1 >= 3):
                pos = (pos[0] - 1, pos[1])
            stdscr.addstr(pos[0],pos[1],"X")
        elif(key=="a"):
            if(pos[1] - 2 >= 0):
                pos = (pos[0], pos[1] - 2)
            stdscr.addstr(pos[0],pos[1],"X")
        elif(key=="s"):
            if(pos[0] + 1 <= stdscr.getmaxyx()[0] - 7):
                pos = (pos[0] + 1, pos[1])
            stdscr.addstr(pos[0],pos[1],"X")
        elif(key=="d"):
            if(pos[1] + 2 <= stdscr.getmaxyx()[1] - 2):
                pos = (pos[0], pos[1] + 2)
            stdscr.addstr(pos[0],pos[1],"X")
        elif(key=="c"):
            stdscr.clear()
            stdscr.addstr(0,printLocation,"{}\n\r".format(message))
            pos = (20,hwidth)
            stdscr.hline(1,0,"=",stdscr.getmaxyx()[1])
            stdscr.hline(stdscr.getmaxyx()[0] - 6,0,"=",stdscr.getmaxyx()[1])
            stdscr.addstr(stdscr.getmaxyx()[0] - 5,0,"Use WASD to control the Etch-A-Sketch\n\rPress c to clear the screen")
            stdscr.addstr(pos[0],pos[1],"")
            
wrapper(main)