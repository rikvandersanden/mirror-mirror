import pigpio

_pi = pigpio.pi()

for pin in range(2, 28):
    print('pin ' + str(pin) + ': ' + str(_pi.read(pin)) + ', mode: ' + str(_pi.get_mode(pin)))