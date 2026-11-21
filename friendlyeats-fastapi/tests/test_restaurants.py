from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
BASE = "/api/v1/restaurants"
PAYLOAD = {"name": "Restaurante Test", "category": "Mexicana", "city": "Puebla", "price": 2}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_restaurant():
    response = client.post(BASE, json=PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Restaurante Test"
    assert body["avgRating"] == 0 and body["numRatings"] == 0
    client.delete(f"{BASE}/{body['id']}")


def test_invalid_price():
    response = client.post(BASE, json={**PAYLOAD, "price": 10})
    assert response.status_code == 422


def test_get_update_delete_flow():
    created = client.post(BASE, json=PAYLOAD).json()
    rid = created["id"]

    assert client.get(f"{BASE}/{rid}").json()["city"] == "Puebla"

    updated = client.patch(f"{BASE}/{rid}", json={"city": "Cholula"})
    assert updated.status_code == 200
    assert updated.json()["city"] == "Cholula"
    assert updated.json()["name"] == "Restaurante Test"

    assert client.delete(f"{BASE}/{rid}").status_code == 204
    assert client.get(f"{BASE}/{rid}").status_code == 404
    assert client.delete(f"{BASE}/{rid}").status_code == 404


def test_list_and_filter():
    created = client.post(BASE, json={**PAYLOAD, "city": "CiudadPrueba"}).json()
    response = client.get(BASE, params={"city": "CiudadPrueba"})
    assert response.status_code == 200
    assert any(r["id"] == created["id"] for r in response.json())
    client.delete(f"{BASE}/{created['id']}")
