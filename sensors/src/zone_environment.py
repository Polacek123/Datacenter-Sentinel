import threading
import time
import random

class ZoneEnvironment:
    def __init__(self, temp_low=20.0, temp_high=26.0, hum_low=40.0, hum_high=60.0):
        self.lock = threading.Lock()
        self.last_update = time.time()
        
        self.current_temp = 22.0
        self.cooling_active = False
        self.current_humidity = 50.0
        
        self.temp_low = temp_low
        self.temp_high = temp_high
        self.hum_low = hum_low
        self.hum_high = hum_high

        # Słownik przechowujący aktualny pobór prądu per szafa {sensor_id: kw_value}
        self.power_loads = {}

    def update_power_load(self, sensor_id, load):
        """Metoda, przez którą czujnik prądu zgłasza swoje zużycie"""
        with self.lock:
            self.power_loads[sensor_id] = load

    def _update_physics(self):
        now = time.time()
        dt = now - self.last_update
        self.last_update = now
        
        if dt <= 0:
            return

        # Obliczamy całkowity pobór prądu w pokoju (w kW)
        # Jeśli nie ma jeszcze odczytów, przyjmujemy bazowe 2.0 kW na pokój
        total_room_power = sum(self.power_loads.values()) if self.power_loads else 2.0

        # --- DYNAMICZNA TEMPERATURA (Wersja Agresywna na Prezentację) ---
        if not self.cooling_active:
            heat_factor = 0.05 * total_room_power
            self.current_temp += (0.01 + heat_factor) * dt
            
            if self.current_temp > self.temp_high:
                self.cooling_active = True
        else:
            cooling_efficiency = 0.4 - (0.03 * total_room_power)
            cooling_efficiency = max(0.05, cooling_efficiency)
            
            self.current_temp -= cooling_efficiency * dt
            if self.current_temp < self.temp_low:
                self.cooling_active = False

        # --- WILGOTNOŚĆ (skorelowana z klimatyzacją) ---
        if self.cooling_active:
            self.current_humidity += random.uniform(-0.15, -0.05) * dt
            if self.current_humidity < self.hum_low:
                self.current_humidity = self.hum_low + random.uniform(0.0, 1.0)
        else:
            if self.current_humidity < self.hum_high:
                self.current_humidity += random.uniform(0.02, 0.06) * dt

    def get_temperature(self):
        with self.lock:
            self._update_physics()
            return self.current_temp

    def get_humidity(self):
        with self.lock:
            self._update_physics()
            return self.current_humidity