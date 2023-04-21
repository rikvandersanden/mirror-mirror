import leds
import colorsys
from time import sleep

MAX_BRIGHTNESS = 255

# Given 5 separate strips:
# Led | Letter
#   0 | f1
#   1 | f2 + 1 
#   2 | am
#   3 | il
#   4 | ar
hue = 1.0
brigthness = 0.5
speed = 2.0

while 1 == 1:
    # show I
    _rgb255 = self.to_255(colorsys.hsv_to_rgb(hue, 1.0, 0.5)))
    leds.set(0, _rgb255)
    sleep(2)

    # show AM
    leds.set(0, (0, 0, 0)))
    leds.set(2, _rgb255)
    sleep(2)

    # show FAMILIAR
    for i in range(5):
        leds.set(i, _rgb255)
    
    sleep(5)

def to_255(rgb):
    return (rgb[0] * MAX_BRIGHTNESS, rgb[1] * MAX_BRIGHTNESS, rgb[2] * MAX_BRIGHTNESS)
