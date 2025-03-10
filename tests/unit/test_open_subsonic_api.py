import unittest
from unittest.mock import MagicMock, patch

from fastapi.responses import JSONResponse
import src.app.database as db
import src.app.open_subsonic_api as api
from src.app.service_layer import fill_track, TrackService, AudioType, USLT


def create_track_entity(id: int, title="") -> db.Track:
    album = db.Album(
        id=id,
        name=f"album{id}",
        total_tracks=1,
    )

    track = db.Track(
        id=id,
        file_path=f"./track{id}.mp3",
        file_size=1984500,
        type="audio/mpeg",
        title=f"track{id}" if title == "" else title,
        album=album,
        plays_count=0,
        cover=b"",
        cover_type="",
        bit_rate=128,
        bits_per_sample=3,
        sample_rate=44100,
        channels=2,
        duration=60,
    )

    return track


class TestOpenSubsonicAPI(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()

    def test_get_song_not_found(self):
        with patch(
            "src.app.service_layer.TrackService.get_song_by_id"
        ) as mock_get_song:
            mock_get_song.return_value = None
            result = api.get_song(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"No such id"}'

    def test_get_song(self):
        with patch(
            "src.app.service_layer.TrackService.get_song_by_id"
        ) as mock_get_song:
            mock_get_song.return_value = fill_track(create_track_entity(id=1501), None)
            result = api.get_song(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200
