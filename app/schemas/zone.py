from pydantic import BaseModel

class ZoneBase(BaseModel):
    name: str
    postal_code: str | None = None

class ZoneCreate(ZoneBase):
    pass

class ZoneResponse(ZoneBase):
    id: int
    
    class Config:
        from_attributes = True