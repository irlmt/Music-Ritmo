from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session

from src.app import database as db

TEST_MP3_FILE = "tracks\\MACAN_-_I_AM_78125758.mp3"
TEST_FLAC_FILE = "tracks\\Atomic Heart\\03. Arlekino (Geoffrey Day Remix).flac"


def init_temp_db() -> Engine:
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        artist = db.Artist(name="present_artist1")
        album = db.Album(
            name="present_album1",
            album_artist_id=None,
            total_tracks=1,
            year="2019",
            cover=bytes(),
            artists=[artist],
        )
        session.add(album)
        session.commit()
        session.refresh(artist)
        session.refresh(album)

        genre = db.Genre(name="present_genre1")
        custom_tag = db.CustomTag(
            name="present_custom1", value="present_value1", updated=False
        )
        track = db.Track(
            file_path="./present_track.mp3",
            file_size=3,
            type="audio/mpeg",
            title="Present",
            album_id=album.id,
            album_artist_id=None,
            album_position=2,
            year="2019",
            plays_count=0,
            cover=bytes(),
            cover_type="",
            bit_rate=10,
            bits_per_sample=10,
            sample_rate=10,
            channels=10,
            duration=10,
            genres=[genre],
            artists=[artist],
            custom_tags=[custom_tag],
        )
        session.add(track)
        session.commit()

        track = db.Track(
            file_path="./already_song.flac",
            file_size=3,
            type="audio/flac",
            title="Already",
            album_id=album.id,
            album_artist_id=None,
            album_position=1,
            year="2020",
            plays_count=0,
            cover=bytes(),
            cover_type="",
            bit_rate=10,
            bits_per_sample=10,
            sample_rate=10,
            channels=10,
            duration=10,
            genres=[genre],
            artists=[artist],
            custom_tags=[custom_tag],
        )
        session.add(track)
        session.commit()

    return engine
