import pytest
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TPE1, TPE2, TALB, TCON, TRCK, TDRC  # type: ignore[attr-defined]

from src.app import db_loading


TEST_MP3_FILE = "tracks/MACAN_-_I_AM_78125758.mp3"
TEST_FLAC_FILE = "tracks/Atomic Heart/03. Arlekino (Geoffrey Day Remix).flac"


@pytest.mark.parametrize(
    "file_name, file_tags, expected_tags",
    [
        (
            "temp",
            (
                "title",
                "artist1",
                "artist1",
                "album",
                "genre1",
                "1",
                "2020",
            ),
            (
                "title",
                ["artist1"],
                "artist1",
                "album",
                ["genre1"],
                1,
                "2020",
            ),
        ),
        (
            "temp",
            (
                "title",
                "artist1, artist2",
                "artist2",
                "album",
                "genre1, genre2",
                "2",
                "2009-2021",
            ),
            (
                "title",
                ["artist1", "artist2"],
                "artist2",
                "album",
                ["genre1", "genre2"],
                2,
                "2009-2021",
            ),
        ),
        (
            "temp",
            (
                "title",
                "artist1; artist2",
                None,
                "album",
                "genre1; genre2",
                "3",
                "2021-2022",
            ),
            (
                "title",
                ["artist1", "artist2"],
                None,
                "album",
                ["genre1", "genre2"],
                3,
                "2021-2022",
            ),
        ),
        (
            "temp",
            (
                "title",
                "artist1\\artist2",
                "artist3",
                "album",
                "genre1\\genre2",
                "0",
                "2020",
            ),
            (
                "title",
                ["artist1", "artist2"],
                "artist3",
                "album",
                ["genre1", "genre2"],
                0,
                "2020",
            ),
        ),
        (
            "temp",
            (
                "title, title2",
                "artist1 artist2",
                "artist3",
                "album",
                "genre1 genre2",
                "-1",
                "2023",
            ),
            (
                "title, title2",
                ["artist1 artist2"],
                "artist3",
                "album",
                ["genre1 genre2"],
                -1,
                "2023",
            ),
        ),
        (
            "temp",
            (None, None, None, None, None, None, None),
            (
                "temp",
                ["Неизвестный исполнитель"],
                None,
                "Неизвестный альбом",
                [],
                None,
                None,
            ),
        ),
        (
            "трек",
            (
                "название",
                "артист1, артист2, artist1",
                "артист2",
                "альбом",
                "поп, рок, jazz",
                "1",
                "2021",
            ),
            (
                "название",
                ["артист1", "артист2", "artist1"],
                "артист2",
                "альбом",
                ["поп", "рок", "jazz"],
                1,
                "2021",
            ),
        ),
    ],
)
def test_extract_metadata_mp3(file_name: str, file_tags, expected_tags):
    (
        exp_title,
        exp_artists,
        exp_album_artist,
        exp_album,
        exp_genres,
        exp_track_number,
        exp_year,
    ) = expected_tags

    audio_info = db_loading.AudioInfo(TEST_MP3_FILE)
    audio = MP3(TEST_MP3_FILE)

    tag_names = [
        "TIT2",
        "TPE1",
        "TPE2",
        "TALB",
        "TCON",
        "TRCK",
        "TDRC",
    ]

    audio_info.file_path = file_name
    for name, value in zip(tag_names, file_tags):
        if value is not None:
            audio[name] = eval(name)(text=[value])  # type: ignore[no-untyped-call]
        elif name in audio.tags:
            audio.pop(name)

    db_loading.extract_metadata_mp3(audio, audio_info)

    assert audio_info.title == exp_title
    assert audio_info.artists == exp_artists
    assert audio_info.album_artist == exp_album_artist
    assert audio_info.album == exp_album
    assert audio_info.genres == exp_genres
    assert audio_info.track_number == exp_track_number
    assert audio_info.year == exp_year


@pytest.mark.parametrize(
    "file_name, file_tags, expected_tags",
    [
        (
            "temp",
            (
                "title",
                "artist1",
                "artist1",
                "album",
                "genre1",
                "1",
                "2020",
            ),
            (
                "title",
                ["artist1"],
                "artist1",
                "album",
                ["genre1"],
                1,
                "2020",
            ),
        ),
        (
            "temp",
            (
                "title",
                ["artist1", "artist2"],
                "artist2",
                "album",
                ["genre1", "genre2"],
                "2",
                "2009-2021",
            ),
            (
                "title",
                ["artist1", "artist2"],
                "artist2",
                "album",
                ["genre1", "genre2"],
                2,
                "2009-2021",
            ),
        ),
        (
            "temp",
            (None, None, None, None, None, None, None),
            (
                "temp",
                ["Неизвестный исполнитель"],
                None,
                "Неизвестный альбом",
                [],
                None,
                None,
            ),
        ),
        (
            "трек",
            (
                "название",
                ["артист 1", "артист 2", "artist1"],
                "артист 2",
                "альбом",
                ["поп", "рок", "jazz"],
                "1",
                "2021",
            ),
            (
                "название",
                ["артист 1", "артист 2", "artist1"],
                "артист 2",
                "альбом",
                ["поп", "рок", "jazz"],
                1,
                "2021",
            ),
        ),
    ],
)
def test_extract_metadata_flac(
    file_name: str,
    file_tags,
    expected_tags,
):
    (
        exp_title,
        exp_artists,
        exp_album_artist,
        exp_album,
        exp_genres,
        exp_track_number,
        exp_year,
    ) = expected_tags

    audio_info = db_loading.AudioInfo(TEST_FLAC_FILE)
    audio = FLAC(TEST_FLAC_FILE)

    tag_names = [
        "TITLE",
        "ARTIST",
        "ALBUMARTIST",
        "ALBUM",
        "GENRE",
        "TRACKNUMBER",
        "DATE",
    ]

    audio_info.file_path = file_name
    for name, value in zip(tag_names, file_tags):
        if value is not None:
            audio[name] = value
        elif name in audio.tags:
            audio.pop(name)

    db_loading.extract_metadata_flac(audio, audio_info)

    assert audio_info.title == exp_title
    assert audio_info.artists == exp_artists
    assert audio_info.album_artist == exp_album_artist
    assert audio_info.album == exp_album
    assert audio_info.genres == exp_genres
    assert audio_info.track_number == exp_track_number
    assert audio_info.year == exp_year
