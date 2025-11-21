from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneResponse
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/zones", tags=["Zones"])

@router.post("/", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED)
def create_zone(zone: ZoneCreate, db: Session = Depends(get_db), current_user = Depends(get_current_admin)):
    """Créer une nouvelle zone (admin only)"""
    db_zone = Zone(**zone.dict())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone

@router.get("/", response_model=List[ZoneResponse])
def get_zones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer toutes les zones"""
    zones = db.query(Zone).offset(skip).limit(limit).all()
    return zones

@router.get("/{zone_id}", response_model=ZoneResponse)
def get_zone(zone_id: int, db: Session = Depends(get_db)):
    """Récupérer une zone par ID"""
    zone = db.query(Zone).filter(Zone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone