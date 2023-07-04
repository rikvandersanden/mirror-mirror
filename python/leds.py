import pigpio

# _pinout = ( 
#    4, 1, 0,
#    18, 15, 14,
#    22, 21, 17,
#    11, 9, 10
#)

_pinout = ( 
    1, 4, 0,
    21, 17, 22,
    8, 25, 7,
    9, 11, 10
)

_pi = pigpio.pi()

def set_frequency(hz):
    for i in _pinout:
        _pi.set_PWM_frequency(i, hz)   

def set(led, rgb):
    index = led * 3
    for i in range(3):
        _pi.set_PWM_dutycycle(_pinout[index + i], rgb[i])

