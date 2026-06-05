import os
import json
import threading
import time

from zone_environment import ZoneEnvironment
from sensor_types.temperature_sensor import TemperatureSensor
from sensor_types.humidity_sensor import HumiditySensor
from sensor_types.power_draw_sensor import PowerDrawSensor

def start_sensor(sensor_class, config, zone):
    """Helper function to create a sensor object with custom config parameters"""
    # Budujemy słownik bazowych argumentów
    kwargs = {
        "sensor_id": config['id'],
        "topic": config['topic'],
        "interval": config.get('interval', 5),
        "zone": zone
    }
    
    # Jeśli to czujnik prądu, przekazujemy mu parametry specyficzne z konfiguracji
    if config['type'] == "power_draw":
        if 'base_load' in config:
            kwargs['base_load'] = float(config['base_load'])
        if 'spike_chance' in config:
            kwargs['spike_chance'] = float(config['spike_chance'])

    sensor = sensor_class(**kwargs)
    sensor.run()

if __name__ == "__main__":
    config_raw = os.getenv("SENSORS_CONFIG", "[]")
    sensors_to_run = json.loads(config_raw)

    print(f"--- Uruchamianie floty: {len(sensors_to_run)} czujników ---")

    # Tworzymy jedną wspólną strefę środowiskową dla kontenera
    shared_zone = ZoneEnvironment()

    for cfg in sensors_to_run:
        sensor_map = {
            "temp": TemperatureSensor,
            "humidity": HumiditySensor,
            "power_draw": PowerDrawSensor
        }
        
        sensor_class = sensor_map.get(cfg['type'])
        
        if sensor_class:
            t = threading.Thread(
                target=start_sensor, 
                args=(sensor_class, cfg, shared_zone), 
                daemon=True
            )
            t.start()
            print(f"Thread started for: {cfg['id']} [{cfg['type']}]")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing sensor group...")