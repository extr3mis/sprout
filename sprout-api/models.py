import RPi.GPIO as GPIO
from adafruit_mcp3xxx.analog_in import AnalogIn

from helpers import *

class AnalogSensor:
    def __init__(self, mcp, channelNumber: int):
        self.channelID = getChannel(channelNumber)
        self.channel = AnalogIn(mcp, self.channelID)

    def voltage(self):
        return self.channel.voltage

    def value(self):
        return

class pHSensor(AnalogSensor):
    def __init__(self, mcp, channelNumber: int):
        super().__init__(mcp, channelNumber)

    def value(self):
        v = self.voltage()
        c1 = -8.363
        c2 = 21.34
        return (c1 * v) + c2

class TDSSensor(AnalogSensor):
    def __init__(self, mcp, channelNumber: int):
        super().__init__(mcp, channelNumber)

    def value(self):
        return (self.voltage() / 3.3) * 1000

class WaterLevelSensor(AnalogSensor):
    def __init__(self, mcp, channelNumber: int, power: int):
        super().__init__(mcp, channelNumber)
        
        self.power = power
        self.isActive = False
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.power, GPIO.OUT)

        self.switch_off()

    def switch_on(self):
        GPIO.output(self.power, 1)
        self.isActive = True

    def switch_off(self):
        GPIO.output(self.power, 0)
        self.isActive = False

    def voltage(self):
        return super().voltage()

    def value(self):
        return (self.voltage() / 3.3) * 100

class Pump:
    def __init__(self, pin: int):
        self.pin = pin
        self.isActive = False

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.deactivate()
    
    def activate(self):
        GPIO.output(self.pin, 1)
        self.isActive = True

    def deactivate(self):
        GPIO.output(self.pin, 0)
        self.isActive = False
    
    def toggle(self):
        if self.isActive: 
            GPIO.output(self.pin, 0)
        else:
            GPIO.output(self.pin, 1)

        self.isActive = not self.isActive