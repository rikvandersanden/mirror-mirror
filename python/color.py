def hue_to_rgb255(hue):
    hue = hue * 3

    if hue < 1: # red to green
        value = int(255 * hue)
        return (255 - value, value, 0)
    elif hue < 2: # green to blue
        value = int(255 * (hue - 1))
        return (0, 255 - value, value)
    else: # blue to red
        value = int(255 * (hue - 2))
        return (value, 0, 255 - value)

if __name__ == '__main__':
    for i in range(1000):
        hue = i / 1000.0
        rgb = hue_to_rgb255(hue)
        print("Hue: " + str(hue) + " RGB: " + str(rgb[0]) + " ," + str(rgb[1]) + ", " + str(rgb[2]))