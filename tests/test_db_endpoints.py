from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_user():
    response = client.post("/users", json={"login": "Ivan", "password": "123", "avatar": "cool"})
    print(response.json())
    assert response.status_code == 200

    response = client.delete(f"/users/{response.json()['id']}")
    assert response.status_code == 200

def test_favourite_track():
    response = client.post("/users", json={"login": "Ivan", "password": "123", "avatar": "cool"})
    print(response.json())
    assert response.status_code == 200

    user_id = response.json()['id']

    response = client.post(f"/users/{user_id}/favourite/tracks/1")
    print(response.json())
    assert response.status_code == 200

    response = client.delete(f"/users/{user_id}/favourite/tracks/1")
    assert response.status_code == 200

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

def test_get_track_album():
    response = client.get("/tracks/2/album")
    print(response.json())
    assert response.status_code == 200

def test_get_track_genres():
    response = client.get("/tracks/1/genres")
    print(response.json())
    assert response.status_code == 200

def test_get_favourite_tracks():
    response = client.get("/users/1/favourite/tracks")
    print(response.json())
    assert response.status_code == 200


def test_get_users():
    response = client.get("/users")
    print(response.json())
    assert response.status_code == 200

def test_get_tracks():
    response = client.get("/tracks")
    print(response.json())
    assert response.status_code == 200

def test_get_artists():
    response = client.get("/artists")
    print(response.json())
    assert response.status_code == 200

def test_get_albums():
    response = client.get("/albums")
    print(response.json())
    assert response.status_code == 200