import unittest
from parameterized import parameterized

import random
import re
from datetime import datetime
from typing import Any, Sequence

import src.app.dto as dto
from src.app.open_subsonic_formatter import OpenSubsonicFormatter as OSFormatter


def get_track(title="track_title", starred=True):
    track = dto.Track(id=random.randint(0, 99999), title=title)

    track.album = "album_name"
    track.album_id = random.randint(0, 99999)

    track.artist = "a1, a2"
    track.artist_id = 1
    track.artists = [dto.ArtistItem(1, "a1"), dto.ArtistItem(2, "a2")]

    track.bit_depth = 3
    track.bit_rate = 128
    track.sampling_rate = 44100
    track.channel_count = 2
    track.duration = 60
    track.file_size = 1984500
    track.path = f"./{title}.mp3"
    track.content_type = "audio/mpeg"

    track.disc_number = 1
    track.track_number = 1

    track.bpm = 140
    track.comment = "comment"

    track.cover_art_id = track.id

    track.play_count = 1

    track.year = 2000
    track.created = datetime.now()
    if starred:
        track.starred = datetime.now()

    track.genre = "pop, rock"
    track.genres = [
        dto.GenreItem("pop"),
        dto.GenreItem("rock"),
    ]

    return track


def get_album(name="album_name", starred=True, song_count=1):
    album = dto.Album(
        id=random.randint(0, 99999),
        name=name,
        song_count=song_count,
        duration=0,
        created=datetime.now(),
    )

    album.cover_art_id = album.id

    album.year = 2000
    if starred:
        album.starred = datetime.now()

    album.artist = "a1, a2"
    album.artist_id = 1
    album.artists = [dto.ArtistItem(1, "a1"), dto.ArtistItem(2, "a2")]

    album.genre = "pop, rock"
    album.genres = [
        dto.GenreItem("pop"),
        dto.GenreItem("rock"),
    ]

    album.play_count = 0
    for i in range(song_count):
        track = get_track(f"track_{i}")
        album.duration += track.duration
        album.play_count += track.play_count
        album.tracks.append(track)

    return album


def get_artist(name="artist_name", starred=True, album_count=1):
    artist = dto.Artist(
        id=random.randint(0, 99999),
        name=name,
    )

    artist.artist_image_url = "http://127.0.0.1/artist.jpg"

    if starred:
        artist.starred = datetime.now()

    for i in range(album_count):
        album = get_album(f"album_{i}")
        artist.albums.append(album)

    return artist


def get_artist_index(name="artist_index", artist_count=1):
    artist_index = dto.ArtistIndex(name=name, artist=[])

    for i in range(artist_count):
        artist = get_artist(f"artist_{i}")
        artist_index.artist.append(artist)

    return artist_index


def get_indexes(
    artist_indexes_count=0, shortcut_count=0, track_count=0, with_ignored_articles=False
):
    indexes = dto.Indexes(
        last_modified=datetime.now(),
        ignored_articles=[],
        artist_index=[],
        shortcuts=[],
        tracks=[],
    )

    if with_ignored_articles:
        indexes.ignored_articles.extend(["A", "The"])

    for i in range(artist_indexes_count):
        artist_index = get_artist_index(f"artist_index_{i}")
        indexes.artist_index.append(artist_index)

    for i in range(shortcut_count):
        artist = get_artist(f"artist_{i}")
        indexes.shortcuts.append(artist)

    for i in range(track_count):
        track = get_track(f"track_{i}")
        indexes.tracks.append(track)

    return indexes


def get_playlist(name="playlist_name", song_count=1):
    playlist = dto.Playlist(
        id=1,
        name=name,
        song_count=song_count,
        duration=0,
        created=datetime.now(),
        changed=datetime.now(),
    )

    for i in range(song_count):
        track = get_track(f"track_{i}")
        playlist.duration += track.duration
        playlist.tracks.append(track)

    playlist.owner = "owner"
    playlist.cover_art_id = playlist.id
    playlist.comment = "comment"
    playlist.public = True

    return playlist


def get_combinaiton(artist_count=0, album_count=0, song_count=0, playlist_count=0):
    artists = []
    albums = []
    tracks = []
    playlists = []

    for i in range(artist_count):
        artist = get_artist(f"artist_{i}")
        artists.append(artist)

    for i in range(album_count):
        album = get_album(f"album_{i}")
        albums.append(album)

    for i in range(song_count):
        track = get_track(f"track_{i}")
        tracks.append(track)

    for i in range(playlist_count):
        playlist = get_playlist(f"playlist_{i}")
        playlists.append(playlist)

    return artists, albums, tracks, playlists


GENRES = [
    dto.Genre(albumCount=1, songCount=2, name="Soundtrack"),
    dto.Genre(albumCount=1, songCount=2, name=""),
    dto.Genre(albumCount=0, songCount=0, name="Pop"),
]

TRACKS = [
    dto.Track(id=1, title="title"),
    get_track(starred=False),
    get_track(starred=True),
]

ALBUMS = [
    dto.Album(
        id=random.randint(0, 99999),
        name="album_name",
        song_count=10,
        duration=0,
        created=datetime.now(),
    ),
    get_album(song_count=0),
    get_album(song_count=20),
    get_album(starred=False),
    get_album(starred=True),
]

ARTISTS = [
    dto.Artist(1, "a1"),
    get_artist(album_count=0),
    get_artist(album_count=20),
    get_artist(starred=False),
    get_artist(starred=True),
]

ARITST_INDEXES = [
    get_artist_index(artist_count=0),
    get_artist_index(artist_count=1),
    get_artist_index(artist_count=10),
]

INDEXES = [
    get_indexes(artist_indexes_count=0, shortcut_count=0, track_count=0),
    get_indexes(artist_indexes_count=1, shortcut_count=1, track_count=1),
    get_indexes(artist_indexes_count=10, shortcut_count=10, track_count=10),
    get_indexes(
        artist_indexes_count=10,
        shortcut_count=10,
        track_count=10,
        with_ignored_articles=True,
    ),
]

PLAYLISTS = [
    dto.Playlist(
        id=1,
        name="playlist_name",
        song_count=0,
        duration=0,
        created=datetime.now(),
        changed=datetime.now(),
    ),
    get_playlist(song_count=0),
    get_playlist(song_count=1),
    get_playlist(song_count=10),
]

COMBINATIONS = [
    ([], [], [], []),
    get_combinaiton(artist_count=0, album_count=0, song_count=0, playlist_count=0),
    get_combinaiton(artist_count=1, album_count=1, song_count=1, playlist_count=1),
    get_combinaiton(artist_count=10, album_count=10, song_count=10, playlist_count=10),
]


def is_iso8601(str: str) -> bool:
    return datetime.fromisoformat(str) is not None


def to_str_or_none(val: Any) -> str | None:
    if val is not None:
        return str(val)
    return None


class TestOpenSubsonicFormatter(unittest.TestCase):
    @parameterized.expand(GENRES)
    def test_format_genre(self, genre: dto.Genre):
        encoded = OSFormatter.format_genre(genre)
        self.check_genre(encoded, genre)

    @parameterized.expand(GENRES)
    def test_format_genre_item(self, genre: dto.Genre):
        genre_item = dto.GenreItem(name=genre.name)
        encoded = OSFormatter.format_genre_item(genre_item)
        self.check_genre_item(encoded, genre_item)

    # https://opensubsonic.netlify.app/docs/responses/genres/
    def test_format_genres(self, genres: Sequence[dto.Genre] = GENRES):
        encoded = OSFormatter.format_genres(genres)
        self.assertIsInstance(encoded.get("genre"), list)
        encoded_genres = encoded["genre"]
        for actual, expected in zip(encoded_genres, genres):
            self.check_genre(actual, expected)

    @parameterized.expand(TRACKS)
    def test_format_track(self, track: dto.Track):
        encoded = OSFormatter.format_track(track)
        self.check_track(encoded, track)

    # https://opensubsonic.netlify.app/docs/responses/songs/
    def test_format_track(self, tracks: Sequence[dto.Track] = TRACKS):
        encoded = OSFormatter.format_tracks(tracks)
        self.assertIsInstance(encoded.get("song"), list)
        encoded_tracks = encoded["song"]
        for actual, expected in zip(encoded_tracks, tracks):
            self.check_track(actual, expected)

    @parameterized.expand(ALBUMS)
    def test_format_album(self, album: dto.Album):
        encoded = OSFormatter.format_album(album)
        self.check_album(encoded, album)

    # https://opensubsonic.netlify.app/docs/responses/albumlist/
    def test_format_albums(self, albums: Sequence[dto.Album] = ALBUMS):
        encoded = OSFormatter.format_albums(albums)
        self.assertIsInstance(encoded.get("album"), list)
        encoded_albums = encoded["album"]
        for actual, expected in zip(encoded_albums, albums):
            self.check_album(actual, expected)

    @parameterized.expand(ARTISTS)
    def test_format_artist(self, artist: dto.Artist):
        encoded = OSFormatter.format_artist(artist)
        self.check_artist(encoded, artist)

    @parameterized.expand(ARITST_INDEXES)
    def test_format_album(self, artist_index: dto.ArtistIndex):
        encoded = OSFormatter.format_artist_index(artist_index)
        self.check_artist_index(encoded, artist_index)

    @parameterized.expand(INDEXES)
    def test_format_indexes(self, indexes: dto.Indexes):
        encoded = OSFormatter.format_indexes(indexes)
        self.check_indexes(encoded, indexes)

    @parameterized.expand(PLAYLISTS)
    def test_format_playlist(self, playlist: dto.Playlist):
        encoded = OSFormatter.format_playlist(playlist)
        self.check_playlist(encoded, playlist)

    # https://opensubsonic.netlify.app/docs/responses/playlists/
    def test_format_playlists(self, playlists: Sequence[dto.Playlist] = PLAYLISTS):
        encoded = OSFormatter.format_playlists(playlists)
        self.assertIsInstance(encoded.get("playlist"), list)
        encoded_playlists = encoded["playlist"]
        for actual, expected in zip(encoded_playlists, playlists):
            self.check_playlist(actual, expected)

    # https://opensubsonic.netlify.app/docs/responses/starred2/
    @parameterized.expand(COMBINATIONS)
    def test_format_combination(
        self,
        artists: Sequence[dto.Artist],
        albums: Sequence[dto.Album],
        tracks: Sequence[dto.Track],
        playlists: Sequence[dto.Playlist],
    ):
        encoded = OSFormatter.format_combination(artists, albums, tracks, playlists)

        self.assertIsInstance(encoded.get("artist"), list)
        self.assertIsInstance(encoded.get("album"), list)
        self.assertIsInstance(encoded.get("song"), list)
        self.assertIsInstance(encoded.get("playlist"), list)

        if len(artists) > 0:
            for actual, expected in zip(encoded.get("artist"), artists):
                self.check_artist(actual, expected)
        if len(albums) > 0:
            for actual, expected in zip(encoded.get("album"), albums):
                self.check_album(actual, expected)
        if len(tracks) > 0:
            for actual, expected in zip(encoded.get("song"), tracks):
                self.check_track(actual, expected)
        if len(playlists) > 0:
            for actual, expected in zip(encoded.get("playlist"), playlists):
                self.check_playlist(actual, expected)

    def check_strict(self, encoded: dict[str, Any], key: str, type, val: Any):
        self.assertIsInstance(encoded.get(key), type)
        self.assertEqual(encoded.get(key), val)

    def check_optional_strict(self, encoded: dict[str, Any], key: str, type, val: Any):
        if val is not None:
            self.assertIsInstance(encoded.get(key), type)
            self.assertEqual(encoded.get(key), val)
        else:
            self.assertIsNone(encoded.get(key))

    def check_optional_iso8601(self, encoded: dict[str, Any], key: str, val: Any):
        if val is not None:
            self.assertIsInstance(encoded.get(key), str)
            self.assertTrue(is_iso8601(encoded.get(key)))
        else:
            self.assertIsNone(encoded.get(key))

    def check_iso8601_strict(self, encoded: dict[str, Any], key: str):
        self.assertIsInstance(encoded.get(key), str)
        self.assertTrue(is_iso8601(encoded.get(key)))

    def check_optional_or_default(
        self, encoded: dict[str, Any], key: str, type, val: Any
    ):
        if val is not None:
            self.assertIsInstance(encoded.get(key), type)
            self.assertEqual(encoded.get(key), val)
        else:
            self.assertIsNotNone(encoded.get(key))

    def check_cover_art(self, encoded: dict[str, Any], cover_art_id: int | None):
        if cover_art_id:
            self.assertIsInstance(encoded.get("coverArt"), str)
            self.assertIn(str(cover_art_id), encoded.get("coverArt"))
        else:
            self.assertIsNone(encoded.get("coverArt"))

    # https://opensubsonic.netlify.app/docs/responses/itemgenre/
    def check_genre_item(self, encoded: dict[str, Any], genre_item: dto.GenreItem):
        self.assertIsInstance(encoded.get("name"), str)
        self.assertEqual(encoded.get("name"), genre_item.name)

    # https://opensubsonic.netlify.app/docs/responses/genre/
    def check_genre(self, encoded: dict[str, Any], genre: dto.Genre):
        self.assertIsInstance(encoded.get("value"), str)
        self.assertIsInstance(encoded.get("songCount"), int)
        self.assertIsInstance(encoded.get("albumCount"), int)

        self.assertEqual(encoded.get("value"), genre.name)
        self.assertEqual(encoded.get("songCount"), genre.songCount)
        self.assertEqual(encoded.get("albumCount"), genre.albumCount)

    def check_artist_item(self, encoded: dict[str, Any], artist_item: dto.ArtistItem):
        self.assertIsInstance(encoded.get("id"), str)
        self.assertIsInstance(encoded.get("name"), str)

        self.assertEqual(encoded.get("id"), str(artist_item.id))
        self.assertEqual(encoded.get("name"), artist_item.name)

        self.check_cover_art(encoded, artist_item.cover_art_id)

        self.check_optional_strict(encoded, "albumCount", int, artist_item.album_count)

        self.check_optional_iso8601(encoded, "starred", artist_item.starred)

    # https://opensubsonic.netlify.app/docs/responses/child/
    def check_track(self, encoded: dict[str, Any], track: dto.Track):
        self.check_strict(encoded, "id", str, str(track.id))
        self.check_strict(encoded, "isDir", bool, False)
        self.check_strict(encoded, "title", str, track.title)

        self.check_optional_strict(encoded, "type", str, "music")

        self.check_optional_strict(
            encoded, "parent", str, to_str_or_none(track.album_id)
        )
        self.check_optional_strict(
            encoded, "albumId", str, to_str_or_none(track.album_id)
        )
        self.check_optional_strict(encoded, "album", str, track.album)
        self.check_optional_strict(
            encoded, "artistId", str, to_str_or_none(track.artist_id)
        )
        self.check_optional_strict(encoded, "artist", str, track.artist)
        self.check_optional_strict(encoded, "track", int, track.track_number)
        self.check_optional_strict(encoded, "year", int, track.year)
        self.check_optional_strict(encoded, "genre", str, track.genre)

        self.check_cover_art(encoded, track.cover_art_id)

        self.check_optional_strict(encoded, "size", int, track.file_size)
        self.check_optional_strict(encoded, "contentType", str, track.content_type)

        self.check_optional_strict(encoded, "path", str, track.path)

        if track.path:
            self.assertIsInstance(encoded.get("suffix"), str)
            self.assertIn(encoded.get("suffix"), track.path)
        else:
            self.assertIsNone(encoded.get("suffix"))

        self.check_optional_strict(encoded, "duration", int, track.duration)
        self.check_optional_strict(encoded, "bitRate", int, track.bit_rate)
        self.check_optional_strict(encoded, "bitDepth", int, track.bit_depth)
        self.check_optional_strict(encoded, "samplingRate", int, track.sampling_rate)
        self.check_optional_strict(encoded, "channelCount", int, track.channel_count)
        self.check_optional_strict(encoded, "playCount", int, track.play_count)
        self.check_optional_strict(encoded, "discNumber", int, track.disc_number)

        self.check_optional_iso8601(encoded, "created", track.created)
        self.check_optional_iso8601(encoded, "starred", track.starred)

        self.check_optional_or_default(encoded, "bpm", int, track.bpm)
        self.check_optional_or_default(encoded, "comment", str, track.comment)

        self.assertIsInstance(encoded.get("genres"), list)
        if len(track.genres) > 0:
            for actual, expected in zip(encoded.get("genres"), track.genres):
                self.check_genre_item(actual, expected)

        self.assertIsInstance(encoded.get("artists"), list)
        if len(track.artists) > 0:
            for actual, expected in zip(encoded.get("artists"), track.artists):
                self.check_artist_item(actual, expected)

    # https://opensubsonic.netlify.app/docs/responses/albumid3withsongs/
    def check_album(self, encoded: dict[str, Any], album: dto.Album):
        self.check_strict(encoded, "id", str, str(album.id))
        self.check_strict(encoded, "name", str, album.name)
        self.check_strict(encoded, "songCount", int, album.song_count)
        self.check_strict(encoded, "duration", int, album.duration)

        self.assertIsInstance(encoded.get("created"), str)
        self.assertTrue(is_iso8601(encoded.get("created")))

        self.check_optional_strict(encoded, "artist", str, album.artist)
        self.check_optional_strict(
            encoded, "artistId", str, to_str_or_none(album.artist_id)
        )

        self.check_cover_art(encoded, album.cover_art_id)

        self.check_optional_strict(encoded, "playCount", int, album.play_count)

        self.check_optional_iso8601(encoded, "starred", album.starred)

        self.check_optional_strict(encoded, "year", int, album.year)
        self.check_optional_strict(encoded, "genre", str, album.genre)

        self.assertIsInstance(encoded.get("genres"), list)
        if len(album.genres) > 0:
            for actual, expected in zip(encoded.get("genres"), album.genres):
                self.check_genre_item(actual, expected)

        self.assertIsInstance(encoded.get("artists"), list)
        if len(album.artists) > 0:
            for actual, expected in zip(encoded.get("artists"), album.artists):
                self.check_artist_item(actual, expected)

        if len(album.tracks) > 0:
            self.assertIsInstance(encoded.get("song"), list)
            for actual, expected in zip(encoded.get("song"), album.tracks):
                self.check_track(actual, expected)
        else:
            self.assertIsNone(encoded.get("song"))

    # https://opensubsonic.netlify.app/docs/responses/artist/
    def check_artist(self, encoded: dict[str, Any], artist: dto.Artist):
        self.check_strict(encoded, "id", str, str(artist.id))
        self.check_strict(encoded, "name", str, artist.name)

        self.check_optional_strict(
            encoded, "artistImageUrl", str, artist.artist_image_url
        )
        self.check_optional_iso8601(encoded, "starred", artist.starred)

        if len(artist.albums) > 0:
            self.assertIsInstance(encoded.get("album"), list)
            for actual, expected in zip(encoded.get("album"), artist.albums):
                self.check_album(actual, expected)
        else:
            self.assertIsNone(encoded.get("album"))

    # https://opensubsonic.netlify.app/docs/responses/indexid3/
    def check_artist_index(
        self, encoded: dict[str, Any], artist_index: dto.ArtistIndex
    ):
        self.check_strict(encoded, "name", str, artist_index.name)

        if len(artist_index.artist) > 0:
            self.assertIsInstance(encoded.get("artist"), list)
            for actual, expected in zip(encoded.get("artist"), artist_index.artist):
                self.check_artist(actual, expected)
        else:
            self.assertIsNone(encoded.get("artist"))

    # https://opensubsonic.netlify.app/docs/responses/indexes/
    def check_indexes(self, encoded: dict[str, Any], indexes: dto.Indexes):
        self.assertIsInstance(encoded.get("ignoredArticles"), str)
        self.assertIsInstance(encoded.get("lastModified"), int)

        for article in indexes.ignored_articles:
            self.assertIn(article, encoded.get("ignoredArticles"))

        if len(indexes.shortcuts) > 0:
            self.assertIsInstance(encoded.get("shortcut"), list)
            for actual, expected in zip(encoded.get("shortcut"), indexes.shortcuts):
                self.check_artist(actual, expected)
        else:
            self.assertIsNone(encoded.get("shortcut"))

        if len(indexes.tracks) > 0:
            self.assertIsInstance(encoded.get("child"), list)
            for actual, expected in zip(encoded.get("child"), indexes.tracks):
                self.check_track(actual, expected)
        else:
            self.assertIsNone(encoded.get("child"))

        if len(indexes.artist_index) > 0:
            self.assertIsInstance(encoded.get("index"), list)
            for actual, expected in zip(encoded.get("index"), indexes.artist_index):
                self.check_artist_index(actual, expected)
        else:
            self.assertIsNone(encoded.get("index"))

    # https://opensubsonic.netlify.app/docs/responses/playlistwithsongs/
    def check_playlist(self, encoded: dict[str, Any], playlist: dto.Playlist):
        self.check_strict(encoded, "id", str, str(playlist.id))
        self.check_strict(encoded, "name", str, playlist.name)
        self.check_strict(encoded, "songCount", int, playlist.song_count)
        self.check_strict(encoded, "duration", int, playlist.duration)
        self.check_iso8601_strict(encoded, "created")
        self.check_iso8601_strict(encoded, "changed")

        self.check_optional_strict(encoded, "comment", str, playlist.comment)
        self.check_optional_strict(encoded, "owner", str, playlist.owner)
        self.check_optional_strict(encoded, "public", bool, playlist.public)

        self.check_cover_art(encoded, playlist.cover_art_id)

        if len(playlist.allowed_users) > 0:
            self.assertIsInstance(encoded.get("allowedUser"), list)
            for actual, expected in zip(
                encoded.get("allowedUser"), playlist.allowed_users
            ):
                self.assertIsInstance(actual, str)
                self.assertEqual(actual, expected)
        else:
            self.assertIsNone(encoded.get("allowedUser"))

        if len(playlist.tracks) > 0:
            self.assertIsInstance(encoded.get("entry"), list)
            for actual, expected in zip(encoded.get("entry"), playlist.tracks):
                self.check_track(actual, expected)
        else:
            self.assertIsNone(encoded.get("entry"))


if __name__ == "__main__":
    unittest.main()
