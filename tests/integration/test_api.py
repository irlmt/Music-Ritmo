import pytest
from sqlmodel import Session, select
from unittest.mock import MagicMock, patch

from src.app import database as db
from src.app import db_loading

from fixtures import session


@pytest.mark.parametrize(
    "id, status_code",
    [
        (1, 200),
        (2, 404),
    ],
)
@patch("os.path.getsize")
def test_get_song(mock_getsize: MagicMock, session: Session, id: int, status_code: int):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    track = session.exec(
        select(db.Track).where(db.Track.file_path == "tracks/t1.mp3")
    ).one()

    assert track.album.name == "al1"


@pytest.mark.parametrize(
    "id, status_code",
    [
        (1, 200),
        (2, 404),
    ],
)
@patch("os.path.getsize")
def test_get_album(
    mock_getsize: MagicMock, session: Session, id: int, status_code: int
):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    album = session.exec(select(db.Album).where(db.Album.name == "al1")).one()

    assert album.total_tracks == 2


@pytest.mark.parametrize(
    "id, status_code",
    [
        (1, 200),
        (2, 404),
    ],
)
@patch("os.path.getsize")
def test_get_artist(
    mock_getsize: MagicMock, session: Session, id: int, status_code: int
):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    artist = session.exec(select(db.Artist).where(db.Artist.name == "ar1")).one()

    assert len(artist.albums) == 2


@patch("os.path.getsize")
def test_get_artists(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    artists = session.exec(select(db.Artist)).all()

    assert len(artists) == 2


@patch("os.path.getsize")
def test_get_albums(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    albums = session.exec(select(db.Album)).all()

    assert len(albums) == 2


@patch("os.path.getsize")
def test_search(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    tracks = session.exec(select(db.Track)).all()
    albums = session.exec(select(db.Album)).all()
    artists = session.exec(select(db.Artist)).all()

    assert len(tracks) == 2
    assert len(albums) == 2
    assert len(artists) == 2


@patch("os.path.getsize")
def test_get_genres(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    genres = session.exec(select(db.Genre)).all()

    assert len(genres) == 2


@patch("os.path.getsize")
def test_get_tracks_by_genre(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    tracks = session.exec(select(db.Track)).all()
    genres = session.exec(select(db.Genre)).all()

    assert len(tracks) == 2
    assert len(genres) == 2


@patch("os.path.getsize")
def test_star(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    session.add(db.User(login="test_user", password="password", avatar="line"))
    session.commit()

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    tracks = session.exec(select(db.Track)).all()
    albums = session.exec(select(db.Album)).all()
    artists = session.exec(select(db.Artist)).all()

    assert len(tracks) == 2
    assert len(albums) == 2
    assert len(artists) == 2


@patch("os.path.getsize")
def test_unstar(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    session.add(db.User(login="test_user", password="password", avatar="line"))
    session.commit()

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    tracks = session.exec(select(db.Track)).all()
    albums = session.exec(select(db.Album)).all()
    artists = session.exec(select(db.Artist)).all()

    assert len(tracks) == 2
    assert len(albums) == 2
    assert len(artists) == 2


@patch("os.path.getsize")
def test_get_starred(mock_getsize: MagicMock, session: Session):
    mock_getsize.return_value = 1

    session.add(db.User(login="test_user", password="password", avatar="line"))
    session.commit()

    audio_info = db_loading.AudioInfo("tracks/t1.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track1"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al1"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 1
    audio_info.year = 2020
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    audio_info = db_loading.AudioInfo("tracks/t2.mp3")
    audio_info.type = "audio/mpeg"
    audio_info.title = "track2"
    audio_info.artists = ["ar1", "ar2"]
    audio_info.album_artist = "ar1"
    audio_info.album = "al2"
    audio_info.genres = ["g1", "g2"]
    audio_info.track_number = 2
    audio_info.year = 2021
    audio_info.cover = bytes()
    audio_info.cover_type = ""
    audio_info.custom_tags = []
    audio_info.bit_rate = 1
    audio_info.bits_per_sample = 1
    audio_info.sample_rate = 1
    audio_info.channels = 1
    audio_info.duration = 1

    db_loading.load_audio_data(audio_info, session)

    tracks = session.exec(select(db.Track)).all()
    albums = session.exec(select(db.Album)).all()
    artists = session.exec(select(db.Artist)).all()

    assert len(tracks) == 2
    assert len(albums) == 2
    assert len(artists) == 2
