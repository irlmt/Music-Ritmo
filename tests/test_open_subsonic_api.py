from src.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_ping():
    response = client.get("/rest/ping")
    assert response.status_code == 200

    rsp = response.json()["subsonic-response"]
    assert rsp["status"] == "ok"
    assert rsp["type"] == "MusicRitmo"
    assert rsp["openSubsonic"] == True
    assert rsp["version"] is not None
    assert rsp["serverVersion"] is not None


def test_getPlaylists():
    response = client.post("/playlists", json={
        "name": "My Playlist",
        "user_id": 1,
        "total_tracks": 10,
        "create_date": "2025-01-01"
    })
    assert response.status_code == 200

    response = client.get("/rest/getPlaylists")
    assert response.status_code == 200

    data = response.json()

    subsonic_response = data["subsonic-response"]
    playlists = subsonic_response["playlists"]["playlist"]
    assert len(playlists) > 0

    playlist = playlists[0]
    assert playlist["name"] == "My Playlist"
    assert playlist["owner"] == 1
    assert playlist["songCount"] == 10
    assert playlist["createDate"] == "2025-01-01"