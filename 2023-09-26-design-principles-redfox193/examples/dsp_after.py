from abc import ABC, abstractmethod


# Defining an interface
class Switchable(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass


class LightBulb(Switchable):
    def turn_on(self):
        print("LightBulb: Turned ON")

    def turn_off(self):
        print("LightBulb: Turned OFF")


class Fan(Switchable):
    def turn_on(self):
        print("Fan: Turned ON")

    def turn_off(self):
        print("Fan: Turned OFF")


class Switch:
    def __init__(self, device):
        self.device = device

    def operate(self):
        print("Switch: Toggle operation")
        # Operates on any device that is Switchable
        self.device.turn_on()