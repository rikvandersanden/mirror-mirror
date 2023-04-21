import os
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
 
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
 
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D22)
 
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
 
# create analog inputs
chan0 = AnalogIn(mcp, MCP.P0)
chan1 = AnalogIn(mcp, MCP.P1)
chan2 = AnalogIn(mcp, MCP.P2)

print('Pot 1: ' + str(chan0.value))
print('Pot 2: ' + str(chan1.value))
print('Pot 3: ' + str(chan2.value))
