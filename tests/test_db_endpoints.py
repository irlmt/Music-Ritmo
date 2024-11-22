from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_add_user():
    response = client.post("/users", json={"login": "Ivan", "password": "123", "avatar": "cool"})
    print(response.json())
    assert response.status_code == 200

def test_add_track():
    response = client.post("/tracks", json={"file_path": "./somewhere", "name": "track0", "duration": "1:40", "plays_count": 0})
    print(response.json())
    assert response.status_code == 200

def test_add_album():
    response = client.post("/albums", json={"name": "good tracks", "total_tracks": "3", "cover_path": "./somewhere"})
    print(response.json())
    assert response.status_code == 200

def test_add_genres():
    response = client.post("/genres", json={"name": "fonk"})
    response = client.post("/genres", json={"name": "pop"})
    response = client.post("/genres", json={"name": "alt"})
    print(response.json())
    assert response.status_code == 200

def test_add_track_with_album():
    response = client.post("/tracks", json={"file_path": "./somewhere", "name": "track1", "album_id": 1, "duration": "2:40", "plays_count": 0})
    print(response.json())
    assert response.status_code == 200

def test_add_track_genre():
    response = client.post("/tracks/1/genres/1")
    response = client.post("/tracks/1/genres/2")
    print(response.json())
    assert response.status_code == 200

def test_add_favourite_track():
    response = client.post("/users/1/favourite/tracks/1")
    print(response.json())
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

def test_get_albums():
    response = client.get("/albums")
    print(response.json())
    assert response.status_code == 200