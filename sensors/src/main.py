import os
import json
import threading
from temp_sensor import TemperatureSensor
from humidity_sensor import HumiditySensor

def start_sensor(sensor_class, config):
    """Helper function to create a sensor object"""
    sensor = sensor_class(
        sensor_id=config['id'],
        topic=config['topic'],
        interval=config.get('interval', 5)
    )
    sensor.run()

if __name__ == "__main__":
    # SENSORS_CONFIG='[{"type": "temp", "id": "T1", "topic": "room/t1"}, ...]'
    config_raw = os.getenv("SENSORS_CONFIG", "[]")
    sensors_to_run = json.loads(config_raw)

    print(f"--- Uruchamianie floty: {len(sensors_to_run)} czujników ---")

    for cfg in sensors_to_run:
        sensor_map = {
            "temp": TemperatureSensor,
            "humidity": HumiditySensor
        }
        
        sensor_class = sensor_map.get(cfg['type'])
        
        if sensor_class:
            t = threading.Thread(
                target=start_sensor, 
                args=(sensor_class, cfg),
                daemon=True
            )
            t.start()
            print(f"Thread started for: {cfg['id']}")
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing sensor group...")