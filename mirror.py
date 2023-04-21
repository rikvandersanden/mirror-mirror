import leds
import switch
import colorsys
from time import sleep

MAX_BRIGHTNESS = 255
brightness = 128

class Controller:
   
    _speed_multiplier = 1.0/1024.0

    def __init__(self):
        self.hue = 0.0
        self.speed = 0.0
        self.offset = 0.0
        self.drift = 0.0
        
    def to_255(self, rgb):
        return (rgb[0] * brightness, rgb[1] * brightness, rgb[2] * brightness)

    def offset_hue(self, hue, offset):
        return (hue + offset) % 1.0

    def normalize(self, rgb):
        _sum = sum(rgb)
        if _sum == 0:
            return rgb
        return (rgb[0] / sum(rgb), rgb[1]/sum(rgb), rgb[2]/sum(rgb))

    def cycle(self):
        for i in range(4):
            _rgb255 = self.to_255(self.normalize(colorsys.hsv_to_rgb(self.offset_hue(self.hue, self.offset * i), 1.0, 1.0)))
            leds.set(i, _rgb255)

        self.hue = (self.hue + self.speed*self._speed_multiplier) % 1.0
        self.offset = (self.offset + self.drift) % 1.0

class Controller2(Controller):

    def __init__(self):
        super().__init__()
        self.hues = [0.0, 0.0, 0.0, 0.0]

    def cycle(self):
        for i in range(4):
            _rgb255 = self.to_255(colorsys.hsv_to_rgb(self.hues[i], 1.0, 1.0))
            leds.set(i, _rgb255)
            delta_speed = i * self.offset
            delta_hue = (self.speed - delta_speed) * self._speed_multiplier
            self.hues[i] = (self.hues[i] + delta_hue) % 1.0

        self.offset = (self.offset + self.drift) % 1.0

no_of_iterations = 255

controller = Controller()
offset = 0.1
speed = 1.5
drift = 0.0001
mode = 0

while 1 == 0: # change to true
    new_mode = switch.read()
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


