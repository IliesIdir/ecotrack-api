"""
Script d'ingestion de donnees REELLES depuis Open-Meteo API
Documentation: https://open-meteo.com/en/docs
Source: Donnees meteorologiques en temps reel
"""

import requests
from app.database import SessionLocal
from app.models.zone import Zone
from app.models.indicator import Indicator
from datetime import datetime

def fetch_meteo_data():
    """Recuperer les donnees meteo depuis Open-Meteo API"""
    print("Recuperation des donnees Open-Meteo...")
    
    # Coordonnees de grandes villes francaises
    cities = [
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "postal": "75001"},
        {"name": "Lyon", "lat": 45.7640, "lon": 4.8357, "postal": "69001"},
        {"name": "Marseille", "lat": 43.2965, "lon": 5.3698, "postal": "13001"},
        {"name": "Toulouse", "lat": 43.6047, "lon": 1.4442, "postal": "31000"},
        {"name": "Nice", "lat": 43.7102, "lon": 7.2620, "postal": "06000"},
    ]
    
    results = []
    
    for city in cities:
        url = "https://api.open-meteo.com/v1/forecast"
        
        params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
            "timezone": "Europe/Paris"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results.append({
                "city": city["name"],
                "postal_code": city["postal"],
                "data": data
            })
            print(f"  - {city['name']}: OK")
            
        except requests.exceptions.RequestException as e:
            print(f"  - {city['name']}: Erreur - {e}")
    
    return results

def ingest_meteo_to_db(db, results):
    """Inserer les donnees meteo dans la base"""
    print(f"\nTraitement de {len(results)} villes...")
    
    count = 0
    
    for result in results:
        # Creer ou recuperer la zone
        zone = db.query(Zone).filter(Zone.postal_code == result["postal_code"]).first()
        if not zone:
            zone = Zone(name=result["city"], postal_code=result["postal_code"])
            db.add(zone)
            db.commit()
            db.refresh(zone)
        
        # Recuperer les donnees actuelles
        current = result["data"].get("current", {})
        current_time = current.get("time")
        
        if not current_time:
            continue
        
        try:
            timestamp = datetime.fromisoformat(current_time)
        except:
            timestamp = datetime.utcnow()
        
        # Temperature
        temp = current.get("temperature_2m")
        if temp is not None:
            indicator = Indicator(
                source="Open-Meteo",
                type="temperature",
                value=round(float(temp), 2),
                unit="°C",
                zone_id=zone.id,
                timestamp=timestamp,
                meta_info=f"Current temperature for {result['city']}"
            )
            db.add(indicator)
            count += 1
        
        # Humidite
        humidity = current.get("relative_humidity_2m")
        if humidity is not None:
            indicator = Indicator(
                source="Open-Meteo",
                type="humidity",
                value=round(float(humidity), 2),
                unit="%",
                zone_id=zone.id,
                timestamp=timestamp,
                meta_info=f"Relative humidity for {result['city']}"
            )
            db.add(indicator)
            count += 1
        
        # Vitesse du vent
        wind = current.get("wind_speed_10m")
        if wind is not None:
            indicator = Indicator(
                source="Open-Meteo",
                type="wind_speed",
                value=round(float(wind), 2),
                unit="km/h",
                zone_id=zone.id,
                timestamp=timestamp,
                meta_info=f"Wind speed at 10m for {result['city']}"
            )
            db.add(indicator)
            count += 1
        
        # Precipitation
        precip = current.get("precipitation")
        if precip is not None:
            indicator = Indicator(
                source="Open-Meteo",
                type="precipitation",
                value=round(float(precip), 2),
                unit="mm",
                zone_id=zone.id,
                timestamp=timestamp,
                meta_info=f"Precipitation for {result['city']}"
            )
            db.add(indicator)
            count += 1
    
    db.commit()
    print(f"OK: {count} mesures meteorologiques ajoutees")
    return count

def main():
    print("=" * 60)
    print("INGESTION DE DONNEES REELLES - OPEN-METEO")
    print("=" * 60)
    print("\nSource: Open-Meteo API (https://open-meteo.com)")
    print("Donnees: Temperature, Humidite, Vent, Precipitations")
    print()
    
    db = SessionLocal()
    
    try:
        results = fetch_meteo_data()
        
        if not results:
            print("\nAucune donnee recuperee.")
            return
        
        print(f"\n{len(results)} villes recuperees depuis Open-Meteo")
        
        total = ingest_meteo_to_db(db, results)
        
        print()
        print("=" * 60)
        print(f"SUCCES: {total} mesures meteorologiques ajoutees!")
        print(f"Total dans la BDD: {db.query(Indicator).count()} indicateurs")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()