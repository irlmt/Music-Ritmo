import unittest
from unittest.mock import MagicMock, patch

from src.app.service_layer import TrackService, AudioType, USLT


class TestTrackService(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.track_service = TrackService(self.session_mock)

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
            mock_audio.__getitem__.side_effect = lambda tag: uslt_tag if tag == 'uslt' else None
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


if __name__ == "__main__":
    unittest.main()
