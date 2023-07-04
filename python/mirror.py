import colorsys
import controller
import leds
import os
import sys
import time

DEBUG = len(sys.argv) > 1 and (sys.argv[1] == "-d" or sys.argv[1] == "--debug")

MAX_BRIGHTNESS = 255
MIN_BRIGHTNESS = 32
NUMBER_OF_LEDS = 4

BRIGHTNESS_MULTIPLIER = 255
SPEED_MULTIPLIER = float(1 << 13)
DRIFT_MULTIPLIER = float(1 << 18)
HUE_MULTIPLIER = float(1 << 16)

brightness = 0.5 # [0.0 .. 1.0]
hue = 0.0        # [0.0 .. 1.0]
offset = 0.0     # [0.0 .. 1.0]
speed = 0.002    # [0.0 .. 1.0]
drift = 0.0001   # [0.0 .. 1.0]

def to_255(rgb):
    return (rgb[0] * brightness * BRIGHTNESS_MULTIPLIER, rgb[1] * brightness * BRIGHTNESS_MULTIPLIER, rgb[2] * brightness * BRIGHTNESS_MULTIPLIER)

def offset_hue(hue, offset):
    return (hue + offset) % 1.0

def normalize(rgb):
    return rgb

    _sum = sum(rgb)
    if _sum == 0:
        return rgb
    return (rgb[0] / sum(rgb), rgb[1]/sum(rgb), rgb[2]/sum(rgb))

def hue_to_rgb255(hue):
    return to_255(normalize(colorsys.hsv_to_rgb(hue, 1.0, 1.0)))

def hue_to_rgb(hue):
    hue = hue * 3

    if hue < 1: # red to green
        return (1.0 - hue, hue, 0)
    elif hue < 2: # green to blue
        return (0, 2.0 - hue, hue - 1.0)
    else: # blue to red
        return (hue - 2.0, 0, 3.0 - hue)

def hue_to_offset_rgb255(i, hue):
    return to_255(hue_to_rgb(offset_hue(hue, offset * i)))
    #return to_255(normalize(colorsys.hsv_to_rgb(offset_hue(hue, offset * i), 1.0, 1.0)))

def set_led_to_offset_rgb255(i, hue):
    leds.set(i, hue_to_offset_rgb255(i, hue))

def update_leds():
    for i in range(NUMBER_OF_LEDS):
        set_led_to_offset_rgb255(i, hue)

#leds.set_frequency(8000)

myController = controller.Controller()
#tic = time.perf_counter()

while True:
    if not(myController.isConnected):
        myController.connect()
    for i in range(100):
        if myController.isConnected:
            myController.try_receive()
            brightness = float(MIN_BRIGHTNESS  + myController.brightness) / (MIN_BRIGHTNESS + MAX_BRIGHTNESS)
            speed = myController.speed / SPEED_MULTIPLIER # check multiplier
            drift = myController.drift / DRIFT_MULTIPLIER # check multiplier. Maybe use log scale?
            hue = hue + myController.deltaHue / HUE_MULTIPLIER 
            if myController.buttonPressed:
                offset = 0.0
        
        if DEBUG:
            os.system('clear') # clear console
            print("Hue: " + str(hue))
            print("Offset: " + str(offset))
            print("Brightness: " + str(brightness))
            print("Speed: " + str(speed * SPEED_MULTIPLIER))
            print("Drift: " + str(drift * DRIFT_MULTIPLIER))
        
        update_leds()
    
        hue = (hue + speed) % 1.0
        offset = (offset + drift) % 1.0
    
        if myController.isConnected:
            myController.try_send(int(hue * 255))

        # toc = time.perf_counter()
        # print(f"{1.0/(toc - tic):0.4f} frames per second")
        # tic = toc

