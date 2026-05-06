import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine

from app.mqtt.listener import listen_mqtt

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creating database tables at startup if they don't exist 
    # When PostgreSQL will be implemented this could/should be repalced
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    mqtt_task = asyncio.create_task(listen_mqtt())
    
    yield # App is running
    
    # On shutdown
    mqtt_task.cancel()
    try:
        await mqtt_task
    except asyncio.CancelledError:
        print("Listener MQTT safly closed.")


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    """Simple Health Check Endpoint"""
    return {
        "status": "online",
        "message": "Backend FastAPI running, MQTT listener active in the background."
    }