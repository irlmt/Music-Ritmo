from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from . import database as db

import os
from mutagen.mp3 import MP3

class AudioInfo:
    def __init__(self,
                 file_path: str,
                 title: str,
                 artist: str,
                 album: str,
                 genre: str,
                 track_number: str,
                 release_date:str,
                 year: str,
                 duration: int):
        self.file_path = file_path
        self.title = title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.track_number = track_number
        self.release_date = release_date
        self.year = year
        self.duration = duration

def scan_directory_for_audio_files(dir):
    data = []

    for root, _, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                audio_file = MP3(file_path)
                if audio_file:
                    info = AudioInfo (
                        file_path=file_path,
                        title=str(audio_file.get("TIT2").text[0]) if "TIT2" in audio_file.tags else "Unknown Title",
                        artist=str(audio_file.get("TPE1").text[0]) if "TPE1" in audio_file.tags else "Unknown Artist",
                        album=str(audio_file.get("TALB").text[0]) if "TALB" in audio_file.tags else "Unknown Album",
                        genre=str(audio_file.get("TCON").text[0]) if "TCON" in audio_file.tags else "Unknown Genre",
                        track_number=str(audio_file.tags.get("TRCK").text[0]) if "TRCK" in audio_file.tags else "Unknown Track",
                        release_date=str(audio_file.tags.get("TDRC").text[0]) if "TDRC" in audio_file.tags else "Unknown Date",
                        year=str(audio_file.tags.get("TYER").text[0]) if "TYER" in audio_file.tags else "Unknown Year",
                        duration=audio_file.info.length
                    )
                    data.append(info)
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")

    return data

def load_audio_data(audio: AudioInfo):
    with Session(db.engine) as session:
        artists = []
        names = audio.artist.split(", ")
        for name in names:
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
                total_tracks=0,
                cover_path="",
                artists=artists
            )
            session.add(album)
            session.commit()
            session.refresh(album)

        genres = []
        names = audio.genre.split(", ")
        for name in names:
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
                release_date=audio.release_date,
                plays_count=0,
                genres=genres,
                artists=artists
            )
            session.add(track)
            session.commit()
            session.refresh(track)