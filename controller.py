import serial
import os

HUE = 1 << 0
BRIGHTNESS = 1 << 1
SPEED = 1 << 2
DRIFT = 1 << 3

BUTTON_PRESSED = 1 << 6
BUTTON_RELEASED = 1 << 7

class Controller:
    def __init__(self):
        # set sensible default for when no controller conected
        self.buttonPressed = False
        self.hue = 0
        self.brightness = 255
        self.speed = 127
        self.drift = 127
        self._ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

        self._ser.flush()
    
    def receive(self):
        while self._ser.in_waiting > 0:
            control = int.from_bytes(self._ser.read(), byteorder='big')

            if control == BUTTON_PRESSED:
                self.buttonPressed = True
                return
            if control == BUTTON_RELEASED:
                self.buttonPressed = False
                return
        
            value = int.from_bytes(self._ser.read(), byteorder='big')
            if control == HUE:
                self.hue = value
            if control == BRIGHTNESS:
                self.brightness = value
            if control == SPEED:
                self.speed = value
            if control == DRIFT:
                self.drift = value
        
    def send(self):
        self._ser.write(bytes([self.hue]))

if __name__ == '__main__':
    controller = Controller()

    while True:
        controller.receive()
        os.system('clear') # clear console
        print("Hue: " + str(controller.hue))
        print("Brightness: " + str(controller.brightness))
        print("Speed: " + str(controller.speed))
        print("Drift: " + str(controller.drift))
        if controller.buttonPressed:
             print("Button pressed")

        controller.hue = (controller.hue + 1) % 256
        controller.send()
