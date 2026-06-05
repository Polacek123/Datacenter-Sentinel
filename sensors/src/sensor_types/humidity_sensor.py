import random
from base_sensor import Sensor

class HumiditySensor(Sensor):
    def __init__(self, *args, zone=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.zone = zone

    def read_data(self):
        if self.zone:
            base_humidity = self.zone.get_humidity()
            noise = random.uniform(-0.2, 0.2)
            return round(base_humidity + noise, 2)
        return round(random.uniform(40.0, 60.0), 2)  # Fallback