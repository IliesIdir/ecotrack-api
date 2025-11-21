# EcoTrack API

Projet API & Web Services - EFREI M1DE1 - 2025  
Ilies Idir

## Description

API REST développée avec FastAPI permettant de suivre et analyser des indicateurs environnementaux locaux. Le système gère plusieurs types de données (qualité de l'air, émissions CO2, température, humidité) pour différentes villes françaises, avec un système d'authentification JWT et des fonctionnalités de filtrage et d'analyse statistique.

## Technologies utilisées

**Backend**
- FastAPI pour l'API REST
- SQLAlchemy comme ORM
- SQLite pour la persistance des données
- JWT (python-jose) pour l'authentification
- Pydantic pour la validation des données

**Frontend**
- HTML/CSS/JavaScript vanilla
- Chart.js pour les visualisations

**Tests**
- pytest pour les tests automatisés

## Installation et lancement
Etapes
# Cloner le repository
git clone https://github.com/IliesIdir/ecotrack-api.git

# Créer l'environnement virtuel et installer les dépendenses 

# Lancer le serveur

L'API est accessible sur `http://127.0.0.1:8000` et la documentation interactive sur `/docs`.

## Mise en place

### Création d'un utilisateur admin
```bash
python update_admin.py
```

Transforme l'utilisateur `admin@ecotrack.com` (mot de passe : `admin123`) en administrateur.

### Ingestion des données

**Données réelles (Open-Meteo API)**

ingest_meteo.py

Ce script récupère en temps réel les données météorologiques (température, humidité, vent, précipitations) pour 5 villes françaises via l'API Open-Meteo. C'est la seule source externe réellement utilisée dans le projet.

**Données de test**
python ingest_data.py

J'ai créé ce script pour générer un volume conséquent de données simulées. Il produit 30 jours de mesures de qualité d'air et 6 mois de données CO2/énergie pour chaque ville. Les valeurs sont générées aléatoirement mais restent dans des fourchettes réalistes basées sur des moyennes françaises. Cette approche était nécessaire pour tester efficacement les fonctionnalités de pagination, de filtrage temporel et de calcul de statistiques sur de gros volumes de données. Une API externe ne pouvait pas fournir suffisamment de données historiques pour valider ces aspects du projet.

### Dashboard web

Ouvrir `frontend/index.html` dans un navigateur. Le dashboard permet de visualiser les données via des graphiques interactifs, de les filtrer, et de créer de nouveaux indicateurs (en tant qu'admin).

## Fonctionnalités principales

**Authentification**
- Inscription et connexion avec génération de token JWT
- Gestion de rôles (user : lecture seule / admin : accès complet)
- Protection des routes par middleware

**Gestion des données**
- CRUD complet pour les zones et indicateurs
- Filtrage par type, zone, et plage de dates
- Pagination des résultats

**Statistiques**
- Calcul de moyennes par zone et type d'indicateur
- Analyse de tendances temporelles (journalières ou mensuelles)

**Tests**
- 5 tests automatisés couvrant l'authentification et les endpoints principaux
```bash
pytest tests/ -v
```

## Endpoints

### Authentification
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion

### Zones
- `GET /zones/` - Liste des zones
- `POST /zones/` - Créer une zone (admin)

### Indicateurs
- `GET /indicators/` - Liste avec filtres (requiert authentification)
- `POST /indicators/` - Créer (admin)
- `PUT /indicators/{id}` - Modifier (admin)
- `DELETE /indicators/{id}` - Supprimer (admin)

Filtres disponibles : type, zone_id, date_from, date_to, skip, limit

### Statistiques
- `GET /stats/averages` - Moyennes par zone et type
- `GET /stats/trend` - Tendances temporelles

## Sources de données

**Open-Meteo API**
- Documentation : https://open-meteo.com/en/docs
- Endpoint : https://api.open-meteo.com/v1/forecast
- Gratuite, sans clé API requise
- Données récupérées : température, humidité, vitesse du vent, précipitations

Cette API a été choisie après avoir constaté que OpenAQ (initialement envisagée) n'est plus accessible gratuitement. Open-Meteo fournit des données météorologiques actualisées régulièrement et couvre efficacement les besoins du projet.

## Difficultés rencontrées

L'API OpenAQ que je comptais utiliser pour les données de qualité d'air n'est plus accessible sans clé API payante (les versions v2 et v3 retournent des erreurs 410 et 401). J'ai donc dû me rabattre sur Open-Meteo pour les données réelles et simuler le reste. 

SQLite a quelques limitations pour un projet de ce type (notamment sur les requêtes complexes et la gestion de la concurrence), mais cela reste largement suffisant pour un projet académique et facilite grandement le déploiement et les tests.

## Améliorations possibles

Avec plus de temps, j'aurais pu par exemple :
- Intégrer davantage de sources de données réelles (APIs gouvernementales pour CO2 et déchets)
- Migrer vers PostgreSQL pour de meilleures performances
- Containeriser l'application avec Docker
- Déployer sur une plateforme cloud

## Remarques

Le projet respecte le cahier des charges :
- Authentification JWT avec rôles
- Deux sources de données (Open-Meteo API + données simulées)
- CRUD complet avec filtrage et pagination
- Endpoints de statistiques
- Tests automatisés
- Interface web fonctionnelle
- Documentation complète

La clé JWT dans `config.py` est à titre de démonstration.