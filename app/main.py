from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Zone, Indicator

# Créer toutes les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EcoTrack API",
    description="API de suivi d'indicateurs environnementaux",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur EcoTrack API"}