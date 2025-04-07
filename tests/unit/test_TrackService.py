from typing import List
import random
import unittest
from unittest.mock import MagicMock, patch
import src.app.database as db
from src.app.service_layer import TrackService, AudioType, USLT
from src.app import dto


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


class TestTrackService(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.track_service = TrackService(self.session_mock)

    def test_get_song_by_id_no_song(self):
        self.track_service.track_db_helper.get_track_by_id = MagicMock(
            return_value=None
        )
        result = self.track_service.get_song_by_id(1, None)
        assert result is None

    def test_get_song_by_id_song_found(self):
        song = create_track_entity(1)
        self.track_service.track_db_helper.get_track_by_id = MagicMock(
            return_value=song
        )
        result = self.track_service.get_song_by_id(1, None)
        assert result is not None
        assert isinstance(result, dto.Track)
        assert result.id == song.id
        assert result.title == song.title
        assert result.album == song.album.name

    def test_get_songs_by_genre_check_return_type(self):
        songs = []
        for i in range(1, 11):
            songs.append(create_track_entity(i))
        self.track_service.track_db_helper.get_tracks_by_genre_name = MagicMock(
            return_value=songs
        )

        result = self.track_service.get_songs_by_genre("Genre")

        assert len(result) == len(songs)
        for i in result:
            assert isinstance(i, dto.Track)

    def test_get_random_songs_empty_list(self):
        self.track_service.track_db_helper.get_all_tracks = MagicMock(return_value=[])
        result = self.track_service.get_random_songs()
        assert len(result) == 0

    def test_get_random_songs_just_random(self):
        songs = []
        size = 5
        for i in range(1, 11):
            songs.append(create_track_entity(i))
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs
        )
        result = self.track_service.get_random_songs(size=size)
        assert len(result) == size
        size = 3
        result = self.track_service.get_random_songs(size=size)
        assert len(result) == size
        size = 7
        result = self.track_service.get_random_songs(size=size)
        assert len(result) == size

    def test_get_random_songs_size_eq_tracks(self):
        songs = []
        size = 10
        for i in range(1, 11):
            songs.append(create_track_entity(i))
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs
        )
        result = self.track_service.get_random_songs(size=size)
        assert len(result) == size

    def test_get_random_songs_size_eq_0(self):
        songs = []
        size = 0
        for i in range(1, 11):
            songs.append(create_track_entity(i))
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs
        )
        result = self.track_service.get_random_songs(size=size)
        assert result == []

    def test_get_random_songs_negative_size(self):
        songs = []
        size = -15
        for i in range(1, 11):
            songs.append(create_track_entity(i))
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs
        )
        result = self.track_service.get_random_songs(size=size)
        assert result == []

    def test_get_random_songs_size_more_than_tracks(self):
        songs = []
        size = 15
        for i in range(1, 11):
            songs.append(create_track_entity(i))
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs
        )
        result = self.track_service.get_random_songs(size=size)
        assert len(result) == len(songs)

    def test_get_random_songs_genre(self):
        songs_with_target_genre = []
        songs_without_target_genre = []
        for i in range(1, 11):
            songs_without_target_genre.append(create_track_entity(i))
        for i in range(11, 16):
            songs_with_target_genre.append(create_track_entity(i))
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs_without_target_genre + songs_with_target_genre
        )
        self.track_service.track_db_helper.get_tracks_by_genre_name = MagicMock(
            return_value=songs_with_target_genre
        )
        result = self.track_service.get_random_songs(genre="Genre")
        assert len(result) == len(songs_with_target_genre)
        for song in result:
            assert isinstance(song, dto.Track)
            assert song.id in [s.id for s in songs_with_target_genre]

    def test_get_random_songs_from_year(self):
        songs = []
        songs_with_target_year = []
        target_year = 2021
        for i in range(1, 11):
            song = create_track_entity(i)
            song.year = "2019"
            songs.append(song)
        for i in range(11, 16):
            song = create_track_entity(i)
            song.year = "2025"
            songs_with_target_year.append(song)
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs + songs_with_target_year
        )
        result = self.track_service.get_random_songs(from_year=str(target_year))
        assert len(result) == len(songs_with_target_year)
        for song in result:
            assert isinstance(song, dto.Track)
            assert song.year >= target_year
            assert song.id in [s.id for s in songs_with_target_year]

    def test_get_random_songs_to_year(self):
        songs = []
        songs_with_target_year = []
        target_year = 2021
        for i in range(1, 11):
            song = create_track_entity(i)
            song.year = "2025"
            songs.append(song)
        for i in range(11, 16):
            song = create_track_entity(i)
            song.year = "2019"
            songs_with_target_year.append(song)
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs + songs_with_target_year
        )
        result = self.track_service.get_random_songs(to_year=str(target_year))
        assert len(result) == len(songs_with_target_year)
        for song in result:
            assert isinstance(song, dto.Track)
            assert song.year <= target_year
            assert song.id in [s.id for s in songs_with_target_year]

    def test_get_random_songs_from_year_to_year(self):
        songs = []
        songs_with_target_year = []
        from_year = 2015
        to_year = 2025
        for i in range(1, 11):
            song = create_track_entity(i)
            song.year = f"{random.randint(1900, 2014)}"
            songs.append(song)

        for i in range(16, 26):
            song = create_track_entity(i)
            song.year = f"{random.randint(2026, 2100)}"
            songs.append(song)

        for i in range(11, 16):
            song = create_track_entity(i)
            song.year = f"{random.randint(2015, 2025)}"
            songs_with_target_year.append(song)
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs + songs_with_target_year
        )
        result = self.track_service.get_random_songs(
            from_year=str(from_year), to_year=str(to_year)
        )
        assert len(result) == len(songs_with_target_year)
        for song in result:
            assert isinstance(song, dto.Track)
            assert song.year <= to_year
            assert song.year >= from_year
            assert song.id in [s.id for s in songs_with_target_year]

    def test_get_random_songs_from_year_eaual_to_year(self):
        songs = []
        songs_with_target_year = []
        target_year = 2025
        for i in range(1, 11):
            song = create_track_entity(i)
            song.year = "2021"
            songs.append(song)

        for i in range(11, 16):
            song = create_track_entity(i)
            song.year = "2025"
            songs_with_target_year.append(song)
        self.track_service.track_db_helper.get_all_tracks = MagicMock(
            return_value=songs + songs_with_target_year
        )
        result = self.track_service.get_random_songs(
            from_year=str(target_year), to_year=str(target_year)
        )
        assert len(result) == len(songs_with_target_year)
        for song in result:
            assert isinstance(song, dto.Track)
            assert song.year == target_year
            assert song.id in [s.id for s in songs_with_target_year]

    def test_extract_lyrics_no_track(self):
        self.track_service.track_db_helper.get_track_by_id = MagicMock(
            return_value=None
        )
        result = self.track_service.extract_lyrics(1)
        assert result is None

    def test_extract_lyrics_mp3(self):
        track = MagicMock()
        track.id = 1
        track.type = "audio/mpeg"
        track.file_path = "path/to/mp3"

        self.track_service.track_db_helper.get_track_by_id = MagicMock(
            return_value=track
        )

        with patch("src.app.service_layer.get_audio_object") as mock_get_audio_object:
            mock_audio = MagicMock()
            mock_audio_type = AudioType.MP3
            uslt_tag = MagicMock(spec=USLT)
            uslt_tag.text = "Test lyrics text"
            uslt_tag.lang = "eng"
            mock_audio.__iter__.return_value = ["uslt"]
            mock_audio.__getitem__.side_effect = lambda tag: (
                uslt_tag if tag == "uslt" else None
            )
            mock_get_audio_object.return_value = (mock_audio, mock_audio_type)
            result = self.track_service.extract_lyrics(1)
            expected = [{"text": ["Test lyrics text"], "lang": "eng"}]
            assert result == expected

    def test_extract_lyrics_flac(self):
        track = MagicMock()
        track.id = 1
        track.type = "audio/flac"
        track.file_path = "path/to/flac"

        self.track_service.track_db_helper.get_track_by_id = MagicMock(
            return_value=track
        )

        with patch("src.app.service_layer.get_audio_object") as mock_get_audio_object:
            mock_audio = MagicMock()
            mock_audio_type = AudioType.FLAC
            mock_audio.tags = {"lyrics": ["Test lyrics text"]}
            mock_get_audio_object.return_value = (mock_audio, mock_audio_type)
            result = self.track_service.extract_lyrics(1)
            expected = [{"text": ["Test lyrics text"]}]
            assert result == expected

    def test_extract_lyrics_flac_no_tags(self):
        track = MagicMock()
        track.id = 1
        track.type = "audio/flac"
        track.file_path = "path/to/flac"

        self.track_service.track_db_helper.get_track_by_id = MagicMock(
            return_value=track
        )

        with patch("src.app.service_layer.get_audio_object") as mock_get_audio_object:
            mock_audio = MagicMock()
            mock_audio_type = AudioType.FLAC
            mock_audio.tags = False
            mock_get_audio_object.return_value = (mock_audio, mock_audio_type)
            result = self.track_service.extract_lyrics(1)
            assert result == []


if __name__ == "__main__":
    unittest.main()
