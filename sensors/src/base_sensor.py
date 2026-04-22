import json
import time
import random
import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod


class Sensor(ABC):
    def __init__(self, sensor_id, topic, broker="localhost", port=1883, interval=5):
        self.sensor_id = sensor_id
        self.topic = topic
        self.interval = interval
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.broker = broker
        self.port = port

    @abstractmethod
    def read_data(self):
        """Method implemented by given sensor"""
        pass

    def run(self):
        self.client.connect(self.broker, self.port)
        print(f"Sesnor {self.sensor_id} connected.")
        
        try:
            while True:
                value = self.read_data() 
                
                payload = {
                    "sensor_id": self.sensor_id,
                    "value": value,
                    "timestamp": int(time.time())
                }

                self.client.publish(self.topic, json.dumps(payload))
                
                time.sleep(self.interval)
        except KeyboardInterrupt:
            self.client.disconnect()