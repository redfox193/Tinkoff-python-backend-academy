class LightBulb:
    def turn_on(self):
        print("LightBulb: Turned ON")

    def turn_off(self):
        print("LightBulb: Turned OFF")


class Switch:
    def __init__(self, bulb):
        self.bulb = bulb

    def operate(self):
        print("Switch: Toggle operation")
        # Directly dependent on a concrete LightBulb
        self.bulb.turn_on()
