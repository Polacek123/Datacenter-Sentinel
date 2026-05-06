from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    MQTT_BROKER: str
    MQTT_TOPIC: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()