import random
from base_sensor import Sensor

class PowerDrawSensor(Sensor):
    def read_data(self):
        return round(random.uniform(100.0, 500.0), 2)