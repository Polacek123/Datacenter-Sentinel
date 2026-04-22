from base_sensor import Sensor

class TemperatureSensor(Sensor):
    def read_data(self):
        return round(random.uniform(20.0, 25.0), 2)