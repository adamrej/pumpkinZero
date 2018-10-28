#PumpkinZero.py
#Project for the Mrs to create a spooky pumpkin
#Using a Raspberyy Pi Zero, Pimoroni Blinkt! and Pimoroni Audio PHat!

#To install Blinkt! curl script
# curl https://get.pimoroni.com/blinkt | bash

import signal
import glob #used for searching fo files
import vlc #used for playing sound
import blinkt #Talking to the PiZer0
import time #used for sleeping etc.
import threading

class LEDThread(threading.Thread):
    
    
    def __init__(self):
        self.running = False
        threading.Thread.__init__(self)
        #Define Pallette Colours
        purple = [136,30,228]
        orange1 = [247,95,28]
        orange2 = [255,154,0]
        green = [133,226,31]
        pink = [255,0,128]
        red = [200,32,14]

        #Define Colour Cycles to be looped through
        self.colourCycles =[
            [purple, purple, purple, purple, green, green, green, green],
            [pink,pink,pink,pink,pink,pink,pink,pink],
            [orange1, orange2, orange1, orange2, orange1, orange2, orange1, orange2],
            [red, red, red, red, purple, purple, purple, purple],
            [red, red, green, green, green, green, red, red],
            [green,orange1,green,orange1,green,orange1,green,orange1]
        ]

        #Timer variables
        self.sleepSeconds = 0
        self.transitionSeconds = 10

        #Lists for keeping track of live colours being fed into the LEDs.
        self.liveColours = [] #record the live colours
        self.deltaColours = [] #Calculate the deltas

        #Brightness of output LEDs
        self.brightness=0.2

    #Function to feed the colour array into the BLINKT
    def setLED(self, brightness, colours):
        #from blinkt import set_pixel, set_brightness, show, clear
        led=0
        
        #blinkt.clear()
        while led<=7:
            #print("Trying to set LED " + str(led) +" to colour R - "+ str(colours[led][0]) + " G - " + str(colours[led][1]) + " B - "+ str(colours[led][2]))
            blinkt.set_pixel(led, colours[led][0],colours[led][1],colours[led][2],brightness) #Set the colours of Blinkt!
            led+=1 #skip to next LED
            pass
        blinkt.show() #activate LEDs

        pass


#Function for the LED Cycles.
    def run(self):
        
        self.running=True

        #Markers for cycling through the colour choice
        totalCycles = len(self.colourCycles) -1
        currentCycle = 0
        
        self.targetColours = self.colourCycles[currentCycle] #Initial colourCycles

        while self.running:
            
            if currentCycle == totalCycles:
                currentCycle = 0
            else:
                currentCycle +=1
            #Set LEDs to current config.
            self.setLED(self.brightness,self.targetColours)
            #feed a new list of LEDs in.
            self.targetColours = self.colourCycles[currentCycle] #Initial colourCycles
            #Sleep on start of loop of programme
            time.sleep(self.sleepSeconds)
    
    def stop(self):
        self.running=False

#function containing the audio playback.
class audioThread(threading.Thread):
    
    
    def run(self):
        self.running = True
        playlist = glob.glob("/home/pi/Code/pumpkinZero/sfx/*.wav")  #TODO - do this from relative filepaths.
        #print(playlist)

        #Repeat the playlist perpetually.
        while self.running:
            #Play each clip in turn.
            for song in playlist:
                player = vlc.MediaPlayer(song)
                player.play()
                #Don't try to play another track until the last one is done.
                while player.is_playing == 1:
                    time.sleep(1)
    
    def stop(self):
        self.running=False

def sigint_handler(signum, frame):
    audio.stop()
    leds.stop()

#handle for Ctrl C
signal.signal(signal.SIGINT, sigint_handler)


#Set up separate threads for 
audio = audioThread()
leds = LEDThread()
audio.start()
leds.start()
