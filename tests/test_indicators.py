from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_admin_token():
    # Helper pour obtenir un token admin
    response = client.post(
        "/auth/login",
        data={
            "username": "admin@ecotrack.com",
            "password": "admin123"
        }
    )
    return response.json()["access_token"]

def test_get_indicators_without_auth():
    # Test d'accès sans authentification
    response = client.get("/indicators/")
    assert response.status_code == 401

def test_get_indicators_with_auth():
    # Test de récupération des indicateurs avec authentification
    token = get_admin_token()
    response = client.get(
        "/indicators/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_indicator():
    # Test de création d'indicateur
    token = get_admin_token()
    response = client.post(
        "/indicators/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "source": "TestSource",
            "type": "test_type",
            "value": 100.0,
            "unit": "test_unit",
            "zone_id": 1
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == 100.0