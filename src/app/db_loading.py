from sqlmodel import Session, select
from . import database as db

import os
import logging
from enum import StrEnum

from mutagen.mp3 import MP3
from mutagen.flac import FLAC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class UnknownTag(StrEnum):
    Title       = "Unknown Title"
    Artist      = "Unknown Artist"
    Album       = "Unknown Album"
    Genre       = "Unknown Genre"

class AudioInfo:
    def __init__(self,
                 file_path: str,
                 title: str,
                 artists: list[str],
                 album: str,
                 genres: list[str],
                 track_number: int | None,
                 year: int | None,
                 duration: int):
        self.file_path = file_path
        self.title = title
        self.artists = artists
        self.album = album
        self.genres = genres
        self.track_number = track_number
        self.year = year
        self.duration = duration

def extract_metadata_mp3(file_path):
    audio_file = MP3(file_path)
    return AudioInfo (
        file_path=file_path,
        title=       str(audio_file["TIT2"]) if "TIT2" in audio_file.tags else UnknownTag.Title,
        artists=     str(audio_file["TPE1"]).split(", ") if "TPE1" in audio_file.tags else [UnknownTag.Artist],
        album=       str((audio_file["TALB"]) if "TALB" in audio_file.tags else UnknownTag.Album),
        genres=      str(audio_file["TCON"]).split(", ") if "TCON" in audio_file.tags else [UnknownTag.Genre],
        track_number=int(audio_file["TRCK"]) if "TRCK" in audio_file.tags else None,
        year=        int(audio_file["TYER"]) if "TYER" in audio_file.tags else None,
        duration=audio_file.info.length
    )

def extract_metadata_flac(file_path):
    audio_file = FLAC(file_path)
    return AudioInfo (
        file_path=file_path,
        title=       str(audio_file["TITLE"][0]) if "TITLE" in audio_file.tags else UnknownTag.Title,
        artists=        (audio_file["ARTIST"]) if "ARTIST" in audio_file.tags else [UnknownTag.Artist],
        album=       str(audio_file["ALBUM"][0]) if "ALBUM" in audio_file.tags else UnknownTag.Album,
        genres=         (audio_file["GENRE"]) if "GENRE" in audio_file.tags else [UnknownTag.Genre],
        track_number=int(audio_file["TRACKNUMBER"][0]) if "TRACKNUMBER" in audio_file.tags else None,
        year=        int(audio_file["YEAR"][0]) if "YEAR" in audio_file.tags else None,
        duration=audio_file.info.length
    )

def scan_directory_for_audio_files(dir) -> list[AudioInfo]:
    data = []

    for root, _, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if file.lower().endswith(".mp3"):
                    info = extract_metadata_mp3(file_path)
                    logger.info(f"Parsed mp3 file {file_path}")
                elif file.lower().endswith(".flac"):
                    info = extract_metadata_flac(file_path)
                    logger.info(f"Parsed flac file {file_path}")
                else:
                    raise Exception("Unsupported file")

                data.append(info)

            except Exception as e:
                    logger.warning(f"Error while parsing file {file_path}: {e}")

    return data

def load_audio_data(audio: AudioInfo):
    with Session(db.engine) as session:
        artists = []
        for name in audio.artists:
            artist = session.exec(select(db.Artist).where(db.Artist.name == name)).first()
            if artist == None:
                artist = db.Artist(name=name)
                session.add(artist)
                session.commit()
                session.refresh(artist)
            artists.append(artist)

        album = session.exec(select(db.Album).where(db.Album.name == audio.album)).first()
        if album == None:
            album = db.Album(
                name=audio.album,
                total_tracks=1,
                year=audio.year,
                cover_path="",
                artists=artists
            )
            session.add(album)
            session.commit()
            session.refresh(album)
        else:
            album.total_tracks = album.total_tracks + 1

        genres = []
        for name in audio.genres:
            genre = session.exec(select(db.Genre).where(db.Genre.name == name)).first()
            if genre == None:
                genre = db.Genre(name=name)
                session.add(genre)
                session.commit()
                session.refresh(genre)
            genres.append(genre)

        track = session.exec(select(db.Track).where(db.Track.file_path == audio.file_path)).first()
        if track == None:
            track = db.Track(
                file_path=audio.file_path,
                title=audio.title,
                album_id=album.id,
                duration=audio.duration,
                year=audio.year,
                plays_count=0,
                genres=genres,
                artists=artists
            )
            session.add(track)
            session.commit()
            session.refresh(track)