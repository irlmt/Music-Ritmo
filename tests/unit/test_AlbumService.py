import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

import src.app.database as db
import src.app.dto as dto
from src.app.service_layer import AlbumService, RequestType


def get_entities(
    i: int, artist_name: str = "abc"
) -> tuple[db.Album, db.Track, db.Artist]:
    album = db.Album(
        id=i,
        name=f"album{i}",
        total_tracks=1,
    )

    track = db.Track(
        id=i,
        file_path=f"./track{i}.mp3",
        file_size=1984500,
        type="audio/mpeg",
        title=f"track{i}",
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
        id=i,
        name=artist_name,
        tracks=[track],
        albums=[album],
    )

    return (album, track, artist)


class TestTrackService(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.album_service = AlbumService(self.session_mock)

    def check_album(
        self,
        received: dto.Album,
        db_album: db.Album,
        with_tracks: bool = False,
    ):
        self.assertEqual(received.id, db_album.id)
        self.assertEqual(received.name, db_album.name)
        if with_tracks:
            self.assertEqual(len(received.tracks), len(db_album.tracks))

    def test_get_album_by_id(self):
        album, track, artist = get_entities(1)

        self.album_service.album_db_helper.get_album_by_id = MagicMock(
            return_value=album
        )

        result: dto.Album | None = self.album_service.get_album_by_id(1)

        self.assertIsNotNone(result)
        self.check_album(result, album, with_tracks=True)

    def test_get_album_by_id_not_found(self):
        self.album_service.album_db_helper.get_album_by_id = MagicMock(
            return_value=None
        )

        result: dto.Album | None = self.album_service.get_album_by_id(1)

        self.assertIsNone(result)

    def test_get_album_list_random_one(self):
        album, _, _ = get_entities(1)

        self.album_service.album_db_helper.get_all_albums = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_album_list(RequestType.RANDOM)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

        self.check_album(result[0], album, with_tracks=False)

    @parameterized.expand(
        [
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 1),
            (1, 2, 1),
            (2, 1, 1),
            (2, 2, 2),
        ]
    )
    def test_get_album_list_random_size(
        self, album_count: int, size: int, res_len: int
    ):
        albums = []
        for i in range(album_count):
            album, _, _ = get_entities(1)
            albums.append(album)

        self.album_service.album_db_helper.get_all_albums = MagicMock(
            return_value=albums
        )

        result = self.album_service.get_album_list(RequestType.RANDOM, size)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), res_len)

    def test_get_album_list_by_name(self):
        album, _, _ = get_entities(1)

        self.album_service.album_db_helper.get_albums_by_name = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_album_list(
            RequestType.BY_NAME, size=1, offset=0
        )

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.check_album(result[0], album, with_tracks=False)

    def test_get_album_list_by_artist(self):
        album, _, _ = get_entities(1)

        self.album_service.album_db_helper.get_all_albums = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_album_list(
            RequestType.BY_ARTIST, size=1, offset=0
        )

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.check_album(result[0], album, with_tracks=False)

    @parameterized.expand(
        [
            (0, 0, []),
            (1, 0, [1]),
            (1, 1, [2]),
            (2, 0, [1, 2]),
        ]
    )
    def test_get_album_list_by_artist_size_offset(
        self, size: int, offset: int, res_ids: list[int]
    ):
        album1, _, _ = get_entities(1)
        album2, _, _ = get_entities(2)

        self.album_service.album_db_helper.get_all_albums = MagicMock(
            return_value=[album1, album2]
        )

        self.album_service.album_db_helper.get_album_artist = MagicMock(
            side_effect=lambda id: dto.Artist(id, name=str(id))
        )

        result = self.album_service.get_album_list(
            RequestType.BY_ARTIST, size=size, offset=offset
        )

        self.assertIsNotNone(result)
        self.assertEqual(len(result), len(res_ids))
        for album in result:
            self.assertIn(album.id, res_ids)

    @parameterized.expand(
        [
            ("2000", "2010", ("2000", "2010", False)),
            ("2010", "2000", ("2000", "2010", True)),
            ("2000", "2000", ("2000", "2000", False)),
        ]
    )
    def test_get_album_list_by_year(
        self,
        from_year: str,
        to_year: str,
        expected_call: tuple[str, str, bool],
        size: int = 10,
        offset: int = 0,
    ):
        album, _, _ = get_entities(1)
        album.year = "2005"

        self.album_service.album_db_helper.get_sorted_by_year_albums = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_album_list(
            RequestType.BY_YEAR,
            size=size,
            offset=offset,
            from_year=from_year,
            to_year=to_year,
        )

        self.album_service.album_db_helper.get_sorted_by_year_albums.assert_called_with(
            expected_call[0], expected_call[1], size, offset, expected_call[2]
        )

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.check_album(result[0], album, with_tracks=False)

    @parameterized.expand(
        [
            ("2000", None),
            (None, "2010"),
            (None, None),
        ]
    )
    def test_get_album_list_by_year_failed(
        self,
        from_year: str | None,
        to_year: str | None,
    ):
        album, _, _ = get_entities(1)
        album.year = "2005"

        self.album_service.album_db_helper.get_all_albums = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_album_list(
            RequestType.BY_YEAR, size=10, offset=0, from_year=from_year, to_year=to_year
        )

        self.assertIsNone(result)

    def test_get_album_list_by_genre(self):
        album, _, _ = get_entities(1)

        self.album_service.album_db_helper.get_albums_by_genre = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_album_list(
            RequestType.BY_GENRE, size=10, offset=0, genre="mygenre"
        )

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.check_album(result[0], album, with_tracks=False)

    def test_get_album_list_by_genre_failed(self):
        album, _, _ = get_entities(1)

        self.album_service.album_db_helper.get_albums_by_genre = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_album_list(
            RequestType.BY_GENRE, size=10, offset=0, genre=None
        )

        self.assertIsNone(result)

    def test_get_sorted_artist_albums(self):
        album, _, _ = get_entities(1)

        self.album_service.album_db_helper.get_sorted_artist_albums = MagicMock(
            return_value=[album]
        )

        result = self.album_service.get_sorted_artist_albums(1)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.check_album(result[0], album, with_tracks=False)


if __name__ == "__main__":
    unittest.main()
