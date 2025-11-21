from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Dict
from app.database import get_db
from app.models.indicator import Indicator
from app.utils.auth import get_current_user

router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("/averages")
def get_averages(
    type: str | None = None,
    zone_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Calculer les moyennes des indicateurs par zone et type
    query = db.query(
        Indicator.zone_id,
        Indicator.type,
        func.avg(Indicator.value).label('average'),
        func.count(Indicator.id).label('count')
    )
    
    # Filtres
    if type:
        query = query.filter(Indicator.type == type)
    if zone_id:
        query = query.filter(Indicator.zone_id == zone_id)
    if date_from:
        query = query.filter(Indicator.timestamp >= date_from)
    if date_to:
        query = query.filter(Indicator.timestamp <= date_to)
    
    results = query.group_by(Indicator.zone_id, Indicator.type).all()
    
    return {
        "data": [
            {
                "zone_id": r.zone_id,
                "type": r.type,
                "average": round(r.average, 2),
                "count": r.count
            }
            for r in results
        ]
    }

@router.get("/trend")
def get_trend(
    type: str,
    zone_id: int | None = None,
    period: str = Query("monthly", regex="^(daily|monthly)$"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Obtenir la tendance des indicateurs par période
    query = db.query(Indicator).filter(Indicator.type == type)
    
    if zone_id:
        query = query.filter(Indicator.zone_id == zone_id)
    
    indicators = query.order_by(Indicator.timestamp).all()
    
    # Regrouper par période
    trends = {}
    for indicator in indicators:
        if period == "monthly":
            key = indicator.timestamp.strftime("%Y-%m")
        else:  # daily
            key = indicator.timestamp.strftime("%Y-%m-%d")
        
        if key not in trends:
            trends[key] = {"values": [], "count": 0}
        
        trends[key]["values"].append(indicator.value)
        trends[key]["count"] += 1
    
    # Calculer les moyennes
    result = []
    for period_key, data in sorted(trends.items()):
        avg_value = sum(data["values"]) / len(data["values"])
        result.append({
            "period": period_key,
            "average": round(avg_value, 2),
            "count": data["count"]
        })
    
    return {
        "type": type,
        "zone_id": zone_id,
        "period": period,
        "data": result
    }