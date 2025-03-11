from datetime import datetime
import unittest
from unittest.mock import MagicMock, patch
from parameterized import parameterized

from fastapi.responses import JSONResponse
import src.app.database as db
import src.app.open_subsonic_api as api
from src.app.service_layer import (
    fill_album,
    fill_artist,
    fill_playlist,
    fill_track,
    TrackService,
    AudioType,
    USLT,
    fill_tracks,
)


def create_playlist_entity(id: int, owner: db.User) -> db.Playlist:
    playlist = db.Playlist(
        id=id,
        name=f"playlist-{id}",
        user_id=owner.id,
        total_tracks=5,
        create_date=datetime.now(),
        user=owner,
    )
    return playlist


def get_entities(id: int) -> tuple[db.Album, db.Track, db.Artist]:
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
        title=f"track{id}",
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

    artist = db.Artist(
        id=id,
        name=f"artist-{id}",
        tracks=[track],
        albums=[album],
    )

    return (album, track, artist)


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

    def test_get_lyrics_by_song_id_not_found(self):
        with patch(
            "src.app.service_layer.TrackService.extract_lyrics"
        ) as mock_get_song:
            mock_get_song.return_value = None
            result = api.get_lyrics_by_song_id(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404

    def test_get_lyrics_by_song_id_found(self):
        with patch(
            "src.app.service_layer.TrackService.extract_lyrics"
        ) as mock_get_song:
            mock_get_song.return_value = [{"text": ["Test Line"], "lang": "eng"}]
            result = api.get_lyrics_by_song_id(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_get_random_songs_not_found(self):
        with patch(
            "src.app.service_layer.TrackService.get_random_songs"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = None
            result = api.get_random_songs(session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"Tracks not found"}'

    def test_get_random_songs(self):
        with patch(
            "src.app.service_layer.TrackService.get_random_songs"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = fill_tracks(
                [create_track_entity(id) for id in range(1, 11)], None
            )
            result = api.get_random_songs(session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_get_artist_not_found(self):
        with patch(
            "src.app.service_layer.ArtistService.get_artist_by_id"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = None
            result = api.get_artist(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"No such id"}'

    def test_get_artist_found(self):
        with patch(
            "src.app.service_layer.ArtistService.get_artist_by_id"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = fill_artist(
                db.Artist(id=1, name="artist-1"),
                None,
                with_albums=True,
                with_songs=True,
            )
            result = api.get_artist(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_get_album_not_found(self):
        with patch(
            "src.app.service_layer.AlbumService.get_album_by_id"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = None
            result = api.get_album(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"No such id"}'

    def test_get_album_found(self):
        with patch(
            "src.app.service_layer.AlbumService.get_album_by_id"
        ) as mock_get_random_songs:
            album, _, _ = get_entities(1)
            mock_get_random_songs.return_value = fill_album(album, None)
            result = api.get_album(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_get_playlist_not_found(self):
        with patch(
            "src.app.service_layer.PlaylistService.get_playlist"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = None
            result = api.get_playlist(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404
            assert result.body == b'{"detail":"No such id"}'

    def test_get_playlist_found(self):
        with patch(
            "src.app.service_layer.PlaylistService.get_playlist"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = fill_playlist(
                create_playlist_entity(
                    1, db.User(id=1, login="login", password="pass", avatar="")
                ),
                None,
            )
            result = api.get_playlist(id=1, session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_create_playlist(self):
        with patch(
            "src.app.service_layer.PlaylistService.create_playlist"
        ) as mock_get_random_songs:
            mock_get_random_songs.return_value = fill_playlist(
                create_playlist_entity(
                    1, db.User(id=1, login="login", password="pass", avatar="")
                ),
                None,
            )
            result = api.create_playlist(name="playlist-1", session=self.session_mock)
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_delete_playlist_valid_user(self):
        with patch(
            "src.app.service_layer.PlaylistService.delete_playlist"
        ) as mock_delete_playlist:
            user = db.User(id=1, login="login", password="pass", avatar="")
            user.playlists.append(
                create_playlist_entity(
                    1, db.User(id=1, login="login", password="pass", avatar="")
                ),
                None,
            )
            result = api.delete_playlist(
                id=1, current_user=user, session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_delete_playlist_not_valid_user(self):
        with patch(
            "src.app.service_layer.PlaylistService.delete_playlist"
        ) as mock_delete_playlist:
            user = db.User(id=1, login="login", password="pass", avatar="")
            result = api.delete_playlist(
                id=1, current_user=user, session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 403

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

    @patch("src.app.db_helpers.TrackDBHelper.get_track_by_id")
    def test_scrobble(self, mock_get_track_by_id):
        track = MagicMock(id=1, plays_count=0)
        mock_get_track_by_id.return_value = track
        result = api.scrobble(id=1, session=self.session_mock)
        self.assertEqual(track.plays_count, 1)
        self.assertEqual(result.status_code, 200)

    @patch("src.app.db_helpers.TrackDBHelper.get_track_by_id")
    def test_scrobble_fail_404(self, mock_get_track_by_id):
        mock_get_track_by_id.return_value = None
        result = api.scrobble(id=1, session=self.session_mock)
        self.assertEqual(result.status_code, 404)

    def test_update_playlist_valid_user(self):
        with patch(
            "src.app.service_layer.PlaylistService.update_playlist"
        ) as mock_update_playlist:
            user = db.User(id=1, login="login", password="pass", avatar="")
            user.playlists.append(
                create_playlist_entity(
                    1, db.User(id=1, login="login", password="pass", avatar="")
                ),
                None,
            )
            result = api.update_playlist(
                playlistId=1, current_user=user, session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 200

    def test_update_playlist_valid_user_not_found(self):
        with patch(
            "src.app.service_layer.PlaylistService.update_playlist"
        ) as mock_update_playlist:
            mock_update_playlist.return_value = False
            user = db.User(id=1, login="login", password="pass", avatar="")
            user.playlists.append(
                create_playlist_entity(
                    1, db.User(id=1, login="login", password="pass", avatar="")
                ),
                None,
            )
            result = api.update_playlist(
                playlistId=1, current_user=user, session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 404

    def test_update_playlist_not_valid_user(self):
        with patch(
            "src.app.service_layer.PlaylistService.update_playlist"
        ) as mock_update_playlist:
            user = db.User(id=1, login="login", password="pass", avatar="")
            result = api.update_playlist(
                playlistId=1, current_user=user, session=self.session_mock
            )
            assert isinstance(result, JSONResponse)
            assert result.status_code == 403
