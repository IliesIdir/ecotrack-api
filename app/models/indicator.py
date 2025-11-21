from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Indicator(Base):
    __tablename__ = "indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)  # Ex: "OpenAQ", "ADEME"
    type = Column(String, nullable=False)  # Ex: "air_quality", "co2", "energy"
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # Ex: "µg/m³", "kg", "kWh"
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    meta_info = Column(String)  # JSON string pour infos supplémentaires    
    # Relation avec la zone
    zone = relationship("Zone", back_populates="indicators")