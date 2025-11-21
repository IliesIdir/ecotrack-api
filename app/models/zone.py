from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    postal_code = Column(String, index=True)
    
    # Relation avec les indicateurs
    indicators = relationship("Indicator", back_populates="zone")