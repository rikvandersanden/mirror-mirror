import pigpio

_pinout = (10,9,11)

_pi = pigpio.pi()

def read():
    a = _pi.read(_pinout[0])
    b = _pi.read(_pinout[1])
    c = _pi.read(_pinout[2])
   
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
