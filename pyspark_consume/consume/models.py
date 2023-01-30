from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class SensorReadings(Base):
    __tablename__ ="environment_readings"

    Id = Column(Integer, primary_key=True, nullable=False)
    window_start = Column(TIMESTAMP(timezone=True), nullable=False)
    window_end = Column(TIMESTAMP(timezone=True), nullable=False)
    device_id = Column(Text, nullable=False)
    temperature = Column(DOUBLE_PRECISION, nullable=False)
    humidity = Column(DOUBLE_PRECISION, nullable=False)
    