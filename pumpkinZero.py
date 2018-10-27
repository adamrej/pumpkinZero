#PumpkinZero.py
#Project for the Mrs to create a spooky pumpkin
#Using a Raspberyy Pi Zero, Pimoroni Blinkt! and Pimoroni Audio PHat!

#To install Blinkt! curl script
# curl https://get.pimoroni.com/blinkt | bash


import blinkt
import time
import colorsys



#Function to feed the colour array into the BLINKT
def setLED(brightness, colours):
    #from blinkt import set_pixel, set_brightness, show, clear
    led=0
    
    blinkt.clear()
    while led<=7:
        print("Trying to set LED " + str(led) +" to colour R - "+ str(colours[led][0]) + " G - " + str(colours[led][1]) + " B - "+ str(colours[led][2]))
        blinkt.set_pixel(led, colours[led][0],colours[led][1],colours[led][2],brightness) #Set the colours of Blinkt!
        led+=1 #skip to next LED
        pass
    blinkt.show() #activate LEDs

    pass


#Define Pallette Colours
purple = [136,30,228]
orange1 = [247,95,28]
orange2 = [255,154,0]
green = [133,226,31]
red = [200,32,14]

#Define Colour Cycles to be looped through
colourCycles =[
    [purple, purple, purple, purple, green, green, green, green],
    [orange1, orange2, orange1, orange2, orange1, orange2, orange1, orange2],
    [red, red, red, red, purple, purple, purple, purple],
    [red, red, green, green, green, green, red, red]
]

#Markers for cycling through the colour choice
totalCycles = len(colourCycles) -1
currentCycle = 0

#Timer variables
sleepSeconds = 5
transitionSeconds = 10

#Lists for keeping track of live colours being fed into the LEDs.
liveColours = [] #record the live colours
deltaColours = [] #Calculate the deltas
targetColours = colourCycles[currentCycle] #Initial colourCycles
liveColours = targetColours

#Brightness
brightness=0.2

#Main Loop
while True:
    #Sleep on start of loop of programme
    time.sleep(sleepSeconds)
    
    if currentCycle == totalCycles:
        currentCycle = 0
    else:
        currentCycle +=1

    
    setLED(brightness,targetColours)
    #feed a new list of LEDs in.
    targetColours = colourCycles[currentCycle] #Initial colourCycles
