from periphery import SPI
import colorsys

spi = SPI("/dev/spidev0.0", 3, 500000)


led1 = (255, 255, 255, 255, 255, 255)
led3 = (255, 255, 0, 0, 0, 0)
led4 = (0, 0, 255, 255, 0, 0)
led2 = (0, 0, 0, 0, 255, 255)

var = 1
res = 255.0
while var == 1:
    h = 0
    while (h < res):
        _rgb = colorsys.hsv_to_rgb(h/res, 1.0, 1.0)

        led2 = (
            int(_rgb[0] * res),
            int(_rgb[0] * res),
            int(_rgb[1] * res),
            int(_rgb[1] * res),
            int(_rgb[2] * res),
            int(_rgb[2] * res))
        data = list((0x96, 0xDF, 0xFF, 0xFF) + led1 + led2 + led3 + led4)
        # print(led4)

        spi.transfer(data)
        h = (h + 1) % res


