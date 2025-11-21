from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import User, Zone, Indicator
from app.routers import auth, zones, indicators, stats

# Créer toutes les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EcoTrack API",
    description="API de suivi d'indicateurs environnementaux",
    version="1.0.0"
)

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth.router)
app.include_router(zones.router)
app.include_router(indicators.router)
app.include_router(stats.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur EcoTrack API"}