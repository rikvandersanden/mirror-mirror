import pigpio
import colorsys

pi = pigpio.pi()
max_brightness = 255
brigtness = max_brightness

pinout = (2,3,4,14,15,18,17,27,22,10,9,11)
    
def set_led(led, rgb):
    index = led * 3
    pi.set_PWM_dutycycle(pinout[index], rgb[0])
    pi.set_PWM_dutycycle(pinout[index + 1], rgb[1])
    pi.set_PWM_dutycycle(pinout[index + 2], rgb[2])

def to_full(rgb):
    return (rgb[0] * brigtness, rgb[1] * brigtness, rgb[2] * brigtness)

def offset_hue(hue, offset):
    return (hue + offset) % brigtness

def cycle(speed, offset, drift):
    hue = 0.0 
    while 1 == 1:
        _rgbFull = to_full(colorsys.hsv_to_rgb(hue, 1.0, 1.0))
        set_led(0, _rgbFull)
        _rgbFull = to_full(colorsys.hsv_to_rgb(offset_hue(hue, offset), 1.0, 1.0))
        set_led(1, _rgbFull)
        _rgbFull = to_full(colorsys.hsv_to_rgb(offset_hue(hue, offset * 2), 1.0, 1.0))
        set_led(2, _rgbFull)
        _rgbFull = to_full(colorsys.hsv_to_rgb(offset_hue(hue, offset * 3), 1.0, 1.0))
        set_led(3, _rgbFull)
        hue = (hue + speed/brigtness) % 1.0
        offset = (offset + drift) % 1.0

cycle(0.2, 0.1, 0.0001)
# set_led(0, (0, 0, 255))
# set_led(1, (0, 255, 0))
# set_led(2, (255, 0, 0))
# set_led(3, (255, 255, 0))

