from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    # Test de l'inscription
    import random
    random_num = random.randint(1000, 9999)
    response = client.post(
        "/auth/register",
        json={
            "email": f"test{random_num}@example.com",
            "username": f"testuser{random_num}",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "email" in data
    assert "id" in data

def test_login():
    # Test de la connexion
    response = client.post(
        "/auth/login",
        data={
            "username": "admin@ecotrack.com",
            "password": "admin123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"