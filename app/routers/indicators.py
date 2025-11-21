from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.database import get_db
from app.models.indicator import Indicator
from app.schemas.indicator import IndicatorCreate, IndicatorUpdate, IndicatorResponse
from app.utils.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/indicators", tags=["Indicators"])

@router.post("/", response_model=IndicatorResponse, status_code=status.HTTP_201_CREATED)
def create_indicator(
    indicator: IndicatorCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_admin)
):
    """Créer un nouvel indicateur (admin only)"""
    indicator_data = indicator.dict()
    if indicator_data.get("timestamp") is None:
        indicator_data["timestamp"] = datetime.utcnow()
    
    db_indicator = Indicator(**indicator_data)
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator

@router.get("/", response_model=List[IndicatorResponse])
def get_indicators(
    skip: int = 0,
    limit: int = 100,
    type: str | None = None,
    zone_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Récupérer les indicateurs avec filtres (authentification requise)
    query = db.query(Indicator)
    
    # Filtres
    if type:
        query = query.filter(Indicator.type == type)
    if zone_id:
        query = query.filter(Indicator.zone_id == zone_id)
    if date_from:
        query = query.filter(Indicator.timestamp >= date_from)
    if date_to:
        query = query.filter(Indicator.timestamp <= date_to)
    
    indicators = query.offset(skip).limit(limit).all()
    return indicators

@router.get("/{indicator_id}", response_model=IndicatorResponse)
def get_indicator(
    indicator_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer un indicateur par ID (authentification requise)"""
    indicator = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return indicator

@router.put("/{indicator_id}", response_model=IndicatorResponse)
def update_indicator(
    indicator_id: int,
    indicator: IndicatorUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    # Mettre à jour un indicateur (admin)
    db_indicator = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not db_indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    
    update_data = indicator.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_indicator, key, value)
    
    db.commit()
    db.refresh(db_indicator)
    return db_indicator

@router.delete("/{indicator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_indicator(
    indicator_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    # Supprimer un indicateur (admin)
    db_indicator = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not db_indicator:
        raise HTTPException(status_code=404, detail="Indicator not found")
    
    db.delete(db_indicator)
    db.commit()
    return None