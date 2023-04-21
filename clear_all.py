import pigpio

_pi = pigpio.pi()

for pin in range(2, 28):
    _pi.write(pin, 0)