import json
from datetime import datetime, timezone
import aiomqtt
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.sensor_reading import SensorReading




async def process_message(payload: str, topic: str):
    try:
        data = json.loads(payload)

        sensor_time = data.get("timestamp")
        if sensor_time:
            dt_timestamp = datetime.fromtimestamp(sensor_time, tz=timezone.utc)
        else:
            dt_timestamp = datetime.now(timezone.utc)
        
        async with SessionLocal() as session:
            new_record = SensorReading(
                sensor_id=data.get("sensor_id", "unknown"),
                value=float(data.get("value", 0.0)),
                timestamp=dt_timestamp
            )
            session.add(new_record)
            await session.commit()

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON received on topic: {topic}")
    except ValueError:
        print(f"Error: Sensor value could not be converted to float on topic: {topic}")
    except Exception as e:
        print(f"Database error on topic {topic}: {e}")



async def listen_mqtt():
    try:
        async with aiomqtt.Client(hostname=settings.MQTT_BROKER) as client:
            await client.subscribe(settings.MQTT_TOPIC)
            print(f"Subscribed to MQTT topic: {settings.MQTT_TOPIC}")
            
            async for message in client.messages:
                payload = message.payload.decode()
                topic = message.topic.value
                print(f"Received on {topic}: {payload}")
                
                await process_message(payload, topic)
                        
    except aiomqtt.MqttError as error:
        print(f"MQTT connection error: {error}")