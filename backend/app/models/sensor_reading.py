from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class SensorReading(Base):
    # Nazwa tabeli w bazie danych
    __tablename__ = "sensor_readings" 
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    sensor_id: Mapped[str] = mapped_column(index=True)
    
    value: Mapped[float] 
    timestamp: Mapped[datetime]