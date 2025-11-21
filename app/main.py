from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Zone, Indicator
from app.routers import auth

# Créer toutes les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EcoTrack API",
    description="API de suivi d'indicateurs environnementaux",
    version="1.0.0"
)

# On inclut les routeurs
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur EcoTrack API"}