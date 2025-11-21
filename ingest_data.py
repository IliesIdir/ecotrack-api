"""
Script d'ingestion de donnees pour EcoTrack
Simule l'import de donnees depuis 2 sources:
1. OpenAQ (qualite de l'air)
2. Fichier CSV ADEME (emissions CO2)
"""

from app.database import SessionLocal
from app.models.zone import Zone
from app.models.indicator import Indicator
from datetime import datetime, timedelta
import random

def create_zones(db):
    """Creer des zones si elles n'existent pas"""
    zones_data = [
        {"name": "Paris Centre", "postal_code": "75001"},
        {"name": "Lyon", "postal_code": "69001"},
        {"name": "Marseille", "postal_code": "13001"},
        {"name": "Toulouse", "postal_code": "31000"},
        {"name": "Nice", "postal_code": "06000"},
    ]
    
    zones = []
    for zone_data in zones_data:
        existing = db.query(Zone).filter(Zone.postal_code == zone_data["postal_code"]).first()
        if not existing:
            zone = Zone(**zone_data)
            db.add(zone)
            zones.append(zone)
        else:
            zones.append(existing)
    
    db.commit()
    return zones

def ingest_air_quality_data(db, zones):
    """Simuler l'ingestion de donnees OpenAQ (qualite de l'air)"""
    print("Ingestion des donnees OpenAQ (qualite de l'air)...")
    
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for zone in zones:
        for day in range(30):
            timestamp = base_date + timedelta(days=day)
            pm25_value = random.uniform(15.0, 75.0)
            
            indicator = Indicator(
                source="OpenAQ",
                type="air_quality",
                value=round(pm25_value, 2),
                unit="ug/m3",
                zone_id=zone.id,
                timestamp=timestamp,
                meta_info=f"PM2.5 measurement for {zone.name}"
            )
            db.add(indicator)
    
    db.commit()
    print(f"OK: {30 * len(zones)} mesures de qualite d'air ajoutees")

def ingest_co2_data(db, zones):
    """Simuler l'ingestion de donnees CSV ADEME (emissions CO2)"""
    print("Ingestion des donnees ADEME (emissions CO2)...")
    
    base_date = datetime.utcnow() - timedelta(days=180)
    
    for zone in zones:
        for month in range(6):
            timestamp = base_date + timedelta(days=month * 30)
            co2_value = random.uniform(800.0, 2500.0)
            
            indicator = Indicator(
                source="ADEME",
                type="co2",
                value=round(co2_value, 2),
                unit="kg",
                zone_id=zone.id,
                timestamp=timestamp,
                meta_info=f"Monthly CO2 emissions for {zone.name}"
            )
            db.add(indicator)
    
    db.commit()
    print(f"OK: {6 * len(zones)} mesures d'emissions CO2 ajoutees")

def ingest_energy_data(db, zones):
    """Simuler l'ingestion de donnees de consommation energetique"""
    print("Ingestion des donnees de consommation energetique...")
    
    base_date = datetime.utcnow() - timedelta(days=180)
    
    for zone in zones:
        for month in range(6):
            timestamp = base_date + timedelta(days=month * 30)
            energy_value = random.uniform(2000.0, 5000.0)
            
            indicator = Indicator(
                source="Open-Meteo",
                type="energy",
                value=round(energy_value, 2),
                unit="kWh",
                zone_id=zone.id,
                timestamp=timestamp,
                meta_info=f"Monthly energy consumption for {zone.name}"
            )
            db.add(indicator)
    
    db.commit()
    print(f"OK: {6 * len(zones)} mesures de consommation energetique ajoutees")

def main():
    """Fonction principale d'ingestion"""
    print("Demarrage de l'ingestion de donnees EcoTrack...")
    
    db = SessionLocal()
    
    try:
        print("Creation/Verification des zones...")
        zones = create_zones(db)
        print(f"OK: {len(zones)} zones disponibles")
        
        ingest_air_quality_data(db, zones)
        ingest_co2_data(db, zones)
        ingest_energy_data(db, zones)
        
        print("Ingestion terminee avec succes!")
        print(f"Total d'indicateurs: {db.query(Indicator).count()}")
        
    except Exception as e:
        print(f"Erreur lors de l'ingestion: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()