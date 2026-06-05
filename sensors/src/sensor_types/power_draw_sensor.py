import random
from base_sensor import Sensor

class PowerDrawSensor(Sensor):
    def __init__(self, *args, zone=None, base_load=2.0, spike_chance=0.05, **kwargs):
        super().__init__(*args, **kwargs)
        self.zone = zone
        self.base_load = base_load
        self.spike_chance = spike_chance
        
        self.current_load = self.base_load
        self.spike_duration = 0

    def read_data(self):
        # 1. Logika generowania obciążenia
        if self.spike_duration > 0:
            self.spike_duration -= 1
            noise = random.uniform(-0.1, 0.3)
        else:
            if random.random() < self.spike_chance:
                self.spike_duration = random.randint(3, 8)
                self.current_load += random.uniform(1.5, 4.0)
            
            # Powrót do normy
            self.current_load += (self.base_load - self.current_load) * 0.2
            noise = random.uniform(-0.05, 0.05)

        self.current_load = max(0.1, self.current_load + noise)
        final_value = round(self.current_load, 2)

        # 2. KLUCZOWE: Raportujemy wygenerowany prąd do fizyki strefy
        if self.zone:
            self.zone.update_power_load(self.sensor_id, final_value)

        return final_value