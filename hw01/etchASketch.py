#!/usr/bin/env python3
import curses
from curses import wrapper


def main(stdscr):
    #initialize the window screen 
    stdscr.clear()
    hwidth = int(stdscr.getmaxyx()[1]/2) #gets the loction of the middle point of the screen
    message = "Etch-A-Sketch"
    printLocation = hwidth - int(len(message)/2)
    stdscr.addstr(0,printLocation,"{}\n\r".format(message))
    pos = (20,hwidth) #creates a initial position tuple
    stdscr.hline(1,0,"=",stdscr.getmaxyx()[1]) #draws a horizontal line at the border of the game
    stdscr.hline(stdscr.getmaxyx()[0] - 6,0,"=",stdscr.getmaxyx()[1])
    stdscr.addstr(stdscr.getmaxyx()[0] - 5,0,"Use WASD to control the Etch-A-Sketch\n\rPress C to clear the screen\n\rPress Q to quit")
    stdscr.addstr(pos[0],pos[1],"") #centers the cursor
    
    #actual game logic
    while True:
        stdscr.refresh()
        key = stdscr.getkey()
        
        if(key=="w"): 
            if(pos[0] - 1 >= 3): #checks the border of the window so you cant draw past it
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
            #Repeats the initializing code
            #I realize this is sloppy coding and I'm sorry
            stdscr.clear()
            stdscr.addstr(0,printLocation,"{}\n\r".format(message))
            pos = (20,hwidth)
            stdscr.hline(1,0,"=",stdscr.getmaxyx()[1])
            stdscr.hline(stdscr.getmaxyx()[0] - 6,0,"=",stdscr.getmaxyx()[1])
            stdscr.addstr(stdscr.getmaxyx()[0] - 5,0,"Use WASD to control the Etch-A-Sketch\n\rPress C to clear the screen\n\rPress Q to quit")
            stdscr.addstr(pos[0],pos[1],"")
        elif(key=="q"):
            break #breaks the while loop and closes the window
            
wrapper(main) #wrapper makes it so your command line isnt hung up after playing the game