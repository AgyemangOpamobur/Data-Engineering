from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class SensorReadings(Base):
    __tablename__ = "Environment_Readings"

    id = Column(Integer, primary_key=True, nullable=False)
    ts = Column(Text, nullable=False)
    device = Column(Text, nullable=False)
    co = Column(DOUBLE_PRECISION, nullable=False)
    humidity = Column(DOUBLE_PRECISION, nullable=False)
    light = Column(Text, nullable=False)
    lpg = Column(Text, nullable=False)
    motion=Column(Text, nullable=False)
    smoke = Column(DOUBLE_PRECISION, nullable=False)
    temp = Column(DOUBLE_PRECISION, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    