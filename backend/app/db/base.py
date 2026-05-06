from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """
    Every database model (like SensorData table) 
    inherits from this Base class so SQLAlchemy knows it exists.
    """
    pass