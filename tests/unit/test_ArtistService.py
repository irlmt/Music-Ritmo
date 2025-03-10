import unittest
from unittest.mock import MagicMock, patch
import src.app.database as db
from src.app.service_layer import ArtistService
from src.app import dto


def create_artist_entity(id: int, name: str = "") -> db.Artist:

    artist = db.Artist(
        id=id,
        name=f"artist-{id}" if name == "" else name,
    )

    return artist


class TestArtistService(unittest.TestCase):
    def setUp(self):
        self.session_mock = MagicMock()
        self.artist_service = ArtistService(self.session_mock)

    def test_get_artist_by_id_no_artist(self):
        self.artist_service.artist_db_helper.get_artist_by_id = MagicMock(
            return_value=None
        )
        result = self.artist_service.get_artist_by_id(1)
        assert result is None

    def test_get_artist_by_id_artist_found(self):
        artist = create_artist_entity(id = 1501)
        self.artist_service.artist_db_helper.get_artist_by_id = MagicMock(return_value=artist)

        result = self.artist_service.get_artist_by_id(1501)
        assert result is not None
        assert isinstance(result, dto.Artist)
        assert result.id == artist.id
        assert result.name == artist.name
        assert len(result.albums) == len(artist.albums)

    def test_join_artists_names_empty_list(self):
        result = self.artist_service.join_artists_names([])
        assert result == ''

    def test_join_artists_names_not_empty_list(self):
        artists = [create_artist_entity(id) for id in range(1, 6)]
        result = self.artist_service.join_artists_names(artists)
        assert result == "artist-1, artist-2, artist-3, artist-4, artist-5"

if __name__ == "__main__":
    unittest.main()
