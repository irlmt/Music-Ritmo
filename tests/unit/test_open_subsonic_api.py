import unittest
from unittest.mock import MagicMock, patch
from parameterized import parameterized

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

    @patch("src.app.db_helpers.TrackDBHelper.get_track_by_id")
    @patch("src.app.utils.bytes_to_image")
    def test_get_cover_art_track(self, mock_get_track_by_id, mock_bytes_to_image):
        track = MagicMock(id=1, type="test")
        mock_get_track_by_id.return_value = track
        mock_bytes_to_image.return_value = MagicMock(format="mock")
        result = api.get_cover_art(id="mf-1", size=None, session=self.session_mock)
        self.assertEqual(result.status_code, 200)

    @patch("src.app.db_helpers.AlbumDBHelper.get_album_by_id")
    @patch("src.app.db_helpers.AlbumDBHelper.get_first_track")
    @patch("src.app.utils.bytes_to_image")
    def test_get_cover_art_album(
        self, mock_get_album_by_id, mock_get_first_track, mock_bytes_to_image
    ):
        album = MagicMock(id=1)
        track = MagicMock(id=1, type="test")
        mock_get_album_by_id.return_value = album
        mock_get_first_track.return_value = track
        mock_bytes_to_image.return_value = MagicMock(format="mock")
        result = api.get_cover_art(id="al-1", size=None, session=self.session_mock)
        self.assertEqual(result.status_code, 200)

    @patch("src.app.db_helpers.ArtistDBHelper.get_artist_by_id")
    @patch("src.app.utils.get_default_cover")
    @patch("src.app.utils.image_to_bytes")
    def test_get_cover_art_artist(
        self, mock_get_artist_by_id, mock_get_default_cover, mock_image_to_bytes
    ):
        artist = MagicMock(id=1)
        mock_get_artist_by_id.return_value = artist
        mock_get_default_cover.return_value = MagicMock(format="mock")
        mock_image_to_bytes.return_value = bytes()
        result = api.get_cover_art(id="ar-1", size=None, session=self.session_mock)
        self.assertEqual(result.status_code, 200)

    @parameterized.expand(
        [
            "mf-1",
            "al-1",
            "ar-1",
            "aa-1",
        ]
    )
    @patch("src.app.db_helpers.TrackDBHelper.get_track_by_id")
    @patch("src.app.db_helpers.AlbumDBHelper.get_album_by_id")
    @patch("src.app.db_helpers.ArtistDBHelper.get_artist_by_id")
    def test_get_cover_art_fail_404(
        self, id, mock_get_track_by_id, mock_get_album_by_id, mock_get_artist_by_id
    ):
        mock_get_track_by_id.return_value = None
        mock_get_album_by_id.return_value = None
        mock_get_artist_by_id.return_value = None
        result = api.get_cover_art(id=id, size=None, session=self.session_mock)
        self.assertEqual(result.status_code, 404)
