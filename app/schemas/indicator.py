from pydantic import BaseModel
from datetime import datetime

class IndicatorBase(BaseModel):
    source: str
    type: str
    value: float
    unit: str
    zone_id: int
    meta_info: str | None = None

class IndicatorCreate(IndicatorBase):
    timestamp: datetime | None = None

class IndicatorUpdate(BaseModel):
    value: float | None = None
    meta_info: str | None = None

class IndicatorResponse(IndicatorBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True