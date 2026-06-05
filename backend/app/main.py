import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.mqtt.listener import listen_mqtt

from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.sensor_reading import SensorReading


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creating database tables at startup if they don't exist
    # PostgreSQL musi być uruchomiony — healthcheck w docker-compose to gwarantuje
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    mqtt_task = asyncio.create_task(listen_mqtt())

    yield  # App is running

    # On shutdown
    mqtt_task.cancel()
    try:
        await mqtt_task
    except asyncio.CancelledError:
        print("Listener MQTT safely closed.")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    """Simple Health Check Endpoint"""
    return {
        "status": "online",
        "message": "Backend FastAPI running, MQTT listener active in the background.",
    }

@app.get("/latest")
async def get_latest_readings(limit: int = 10):
    """Diagnostyczny endpoint zwracający ostatnie odczyty."""
    async with SessionLocal() as session:
        result = await session.execute(
            select(SensorReading).order_by(SensorReading.timestamp.desc()).limit(limit)
        )
        readings = result.scalars().all()
        
        return {"readings": readings}