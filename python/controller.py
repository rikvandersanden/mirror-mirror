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
        self.deltaHue = 0
        self.brightness = 255
        self.speed = 127
        self.drift = 127
        self.isConnected = False
    
    def connect(self):
        for p in ('/dev/ttyACM0', '/dev/ttyACM1'):
            if self.try_connect(p):
                self.isConnected = True
                return
        
        self.isConnected = False

    def try_connect(self, port):
        if os.path.exists(port):
            self._ser = serial.Serial(port, 9600, timeout=1)
            self._ser.flush()
            return True
        return False

    def try_receive(self):
        try:
            self.receive()
        except:
            self.isConnected = False

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
                self.deltaHue = value - 128
            if control == BRIGHTNESS:
                self.brightness = value
            if control == SPEED:
                self.speed = value
            if control == DRIFT:
                self.drift = value
    
    def try_send(self, hue):
        try:
            self.send(hue)
        except:
            self.isConnected = False

    def send(self, hue):
        self._ser.write(bytes([int(hue)]))

if __name__ == '__main__':
    controller = Controller()
    controller.connect()

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
