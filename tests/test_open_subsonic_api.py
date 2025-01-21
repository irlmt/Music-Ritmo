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


def test_get_tracks_by_genre():
    response = client.get("/rest/genres/Soundtrack/tracks")

    assert response.status_code == 200
    data = response.json()["subsonic-response"]
    assert "track" in data
    assert len(data["track"]) == 2

    first_track = {'id': '5', 'parent': '', 'title': 'Arlekino (Geoffrey Day Remix)', 'isDir': False,
                   'isVideo': False, 'type': 'audio/flac', 'albumId': '3',
                   'album': "id=3 year='2023' name='Atomic Heart (Original Game Soundtrack)' total_tracks=2",
                   'artistId': '', 'artist': '', 'coverArt': None, 'duration': 262.25895691609975, 'bitRate': 0,
                   'bitDepth': 16, 'samplingRate': 44100, 'channelCount': 2, 'userRating': 0, 'averageRating': 0.0,
                   'track': 1, 'year': 2023, 'genre': None, 'size': 0, 'discNumber': 1, 'suffix': '',
                   'contentType': 'audio/mpeg',
                   'path': './tracks/Atomic Heart/03. Arlekino (Geoffrey Day Remix).flac'}

    second_track = {'id': '6', 'parent': '', 'title': 'Trava u Doma (Geoffrey Day Remix)', 'isDir': False,
                    'isVideo': False, 'type': 'audio/flac', 'albumId': '3',
                    'album': "id=3 year='2023' name='Atomic Heart (Original Game Soundtrack)' total_tracks=2",
                    'artistId': '', 'artist': '', 'coverArt': None, 'duration': 235.682947845805, 'bitRate': 0,
                    'bitDepth': 16, 'samplingRate': 44100, 'channelCount': 2, 'userRating': 0, 'averageRating': 0.0,
                    'track': 1, 'year': 2023, 'genre': None, 'size': 0, 'discNumber': 1, 'suffix': '',
                    'contentType': 'audio/mpeg',
                    'path': './tracks/Atomic Heart/02. Trava u Doma (Geoffrey Day Remix).flac'}

    assert [first_track, second_track] == data["track"]
