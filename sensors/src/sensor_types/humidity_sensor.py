import random
from base_sensor import Sensor

class HumiditySensor(Sensor):
    def read_data(self):
        return round(random.uniform(40.0, 60.0), 2)