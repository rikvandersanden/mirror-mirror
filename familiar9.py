import leds
import colorsys
from time import sleep

MAX_BRIGHTNESS = 255
brightness = 0.5
NUMBER_OF_LEDS = 8

class Controller:
   
    _speed_multiplier = 1.0/1024.0

    def __init__(self):
        self.hue = 0.0
        self.speed = 0.0
        self.offset = 0.0
        self.drift = 0.0
        
    def to_255(self, rgb):
        return (rgb[0] * MAX_BRIGHTNESS, rgb[1] * MAX_BRIGHTNESS, rgb[2] * MAX_BRIGHTNESS)

    def offset_hue(self, hue, offset):
        return (hue + offset) % 1.0

    def normalize(self, rgb):
        _sum = sum(rgb)
        if _sum == 0:
            return rgb
        return (rgb[0] / sum(rgb), rgb[1]/sum(rgb), rgb[2]/sum(rgb))

    def hue_to_rgb255(self, hue):
        return self.to_255(self.normalize(colorsys.hsv_to_rgb(hue, 1.0, brightness)))

    def hue_to_offset_rgb255(self, i, hue):
        return self.to_255(self.normalize(colorsys.hsv_to_rgb(self.offset_hue(hue, self.offset * i), 1.0, brightness)))

    def set_led_to_offset_rgb255(self, i, hue):
        leds.set(i, self.hue_to_offset_rgb255(i, self.hue))

    def cycle(self):
        for i in range(NUMBER_OF_LEDS):
            self.set_led_to_offset_rgb255(i, self.hue)
            
        self.hue = (self.hue + self.speed*self._speed_multiplier) % 1.0
        self.offset = (self.offset + self.drift) % 1.0

    def mirror_flow(self):
        for i in range(NUMBER_OF_LEDS):
            self.set_led_to_offset_rgb255(i, self.hue)

    def i_am_familiar(self):
        leds.partial_f()
        for i in range(NUMBER_OF_LEDS):
            leds.set(i, (0,0,0))
        
        leds.set(0, self.hue_to_rgb255(self.hue))
        sleep(2)

        for i in range(3):
            leds.set(i, self.hue_to_rgb255(self.hue))

        sleep(2)

        leds.full_f()
        for i in range(NUMBER_OF_LEDS):
            leds.set(i, self.hue_to_rgb255(self.hue))

        sleep(4)

    def set_mirror_mode(self):
        self.offset = 0.1
        self.drift = 0.0001

    def set_rainbow_mode(self):
        self.offset = 0.1
        self.drift = 0.0

    def set_uniform_mode(self):
        self.speed = 0.0
        self.offset = 0.0
        self.drift = 0.0

no_of_iterations = 65536

controller = Controller()
offset = 0.1
speed = 2.0
drift = 0.0001

controller.speed = speed
controller.offset = offset
controller.drift = drift

for i in range(NUMBER_OF_LEDS):
    for j in range(NUMBER_OF_LEDS):
        if i==j:
            leds.set(j, (128, 128, 128))
        else:
            leds.set(j, (0, 0, 0) )
    sleep (0.2)

while 1 == 1:
    controller.set_uniform_mode()
    for j in range(4):
        controller.i_am_familiar() # uses sleep, so this is the actual number of iterations

    controller.set_rainbow_mode()
    controller.speed = 16.0
    for i in range(255):
        controller.cycle()

    for i in range(NUMBER_OF_LEDS):
        for j in range(NUMBER_OF_LEDS):
            if i==j:
                leds.set(j, controller.hue_to_rgb255(controller.hue))
            else:
                leds.set(j, (0,0,0))
        sleep (0.2)

    controller.speed = 2.0
    controller.set_mirror_mode()
    for i in range(255):
        controller.cycle()