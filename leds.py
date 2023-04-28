import pigpio

_pinout = ( 19,21,16,
            18,17,23,
            20,26,13,
            27, 4,22,
            5, 6, 12)

_pi = pigpio.pi()

def set(led, rgb):
    index = led * 3
    for i in range(3):
        _pi.set_PWM_dutycycle(_pinout[index + i], rgb[i])

def write(pin):
    _pi.write(pin, 0)
