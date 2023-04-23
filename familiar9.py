import leds
import colorsys
from time import sleep

MAX_BRIGHTNESS = 255
brightness = 0.5
NUMBER_OF_LEDS = 5

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

    def cycle(self):
        for i in range(NUMBER_OF_LEDS):
            _rgb255 = self.to_255(self.normalize(colorsys.hsv_to_rgb(self.offset_hue(self.hue, self.offset * i), 1.0, brightness)))
            leds.set(i, _rgb255)

        self.hue = (self.hue + self.speed*self._speed_multiplier) % 1.0
        self.offset = (self.offset + self.drift) % 1.0

class Controller2(Controller):

    def __init__(self):
        super().__init__()
        self.hues = [0.0, 0.0, 0.0, 0.0]

    def cycle(self):
        for i in range(NUMBER_OF_LEDS):
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

controller.speed = speed
controller.offset = offset
controller.drift = drift

while 1 == 1: 
    controller.cycle()