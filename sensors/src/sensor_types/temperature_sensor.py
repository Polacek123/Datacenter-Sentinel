import random
from base_sensor import Sensor

class TemperatureSensor(Sensor):
    def __init__(self, *args, zone=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.zone = zone  # Referencja do współdzielonej strefy

    def read_data(self):
        if self.zone:
            base_temp = self.zone.get_temperature()
            # Czujnik dodaje malutki szum pomiarowy specyficzny dla niego
            noise = random.uniform(-0.05, 0.05)
            return round(base_temp + noise, 2)
        return round(random.uniform(20.0, 25.0), 2)  # Fallback