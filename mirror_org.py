import pigpio
import colorsys
from time import sleep

pi = pigpio.pi()
switch_pins = (16 ,20, 21)
pinout = (2,3,4,14,15,18,17,27,22,10,9,11)

MAX_BRIGHTNESS = 255
brightness = MAX_BRIGHTNESS

class Controller:

    def __init__(self):
        self.hue = 0.0
        self.speed = 0.0
        self.offset = 0.0
        self.drift = 0.0
        
    def set_led(self, led, rgb):
        index = led * 3
        for i in range(3):
            pi.set_PWM_dutycycle(pinout[index + i], rgb[i])

    def to_full(self, rgb):
        return (rgb[0] * brightness, rgb[1] * brightness, rgb[2] * brightness)

    def offset_hue(self, hue, offset):
        return (hue + offset) % brightness

    def cycle(self):
        for i in range(4):
            _rgbFull = self.to_full(colorsys.hsv_to_rgb(self.offset_hue(self.hue, self.offset * i), 1.0, 1.0))
            self.set_led(i, _rgbFull)

        self.hue = (self.hue + self.speed/brightness) % 1.0
        self.offset = (self.offset + self.drift) % 1.0

def read_switch():
    a = pi.read(switch_pins[0])
    b = pi.read(switch_pins[1])
    c = pi.read(switch_pins[2])
    
    if b:
        if a:
            return 2
        if c:
            return 4
        return 3
    if a:
        return 1
    if c:
        return 5
    return 0

no_of_iterations = 255

controller = Controller()
offset = 0.1
speed = 0.2
drift = 0.0001
mode = 0

while 1 == 1:
    new_mode = read_switch()
    if not new_mode == mode:
        mode = new_mode
        print('switching to mode %d' % mode)
        if mode == 1: # constant solid color
            controller.speed = 0
        elif mode == 2: # fading solid color
            controller.speed = speed
            controller.offset = 0
        elif mode == 3: # fading with offset
            controller.offset = offset
            controller.drift = 0
        elif mode == 4: # fading with drifting offset
            controller.speed = speed
            controller.drift = drift
        else: # freeze
            controller.speed = 0
            controller.drift = 0
    controller.cycle()
    if (mode == 1 or mode == 5): # for static modes, take a nap
        sleep(1)    


