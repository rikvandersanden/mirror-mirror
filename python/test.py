import leds
from time import sleep

for i in range(12):
    leds._pi.set_PWM_dutycycle(leds._pinout[i], 0)
    
for i in range(12):
    leds._pi.set_PWM_dutycycle(leds._pinout[i], 255)
    sleep(1)
    leds._pi.set_PWM_dutycycle(leds._pinout[i], 0)
