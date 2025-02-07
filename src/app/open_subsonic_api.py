from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

from . import database as db
from . import service_layer

open_subsonic_router = APIRouter(prefix="/rest", )


class SubsonicResponse:
    def __init__(self):
        self.data = {
            "status": "ok",
            "version": "1.16.1",
            "type": "MusicRitmo",
            "serverVersion": "0.1",
            "openSubsonic": True,
        }

    def to_json_rsp(self) -> JSONResponse:
        return JSONResponse({"subsonic-response": self.data})


class SubsonicTrack(BaseModel):
    id: str = Field(default_factory=str)
    parent: str = Field(default_factory=str)
    title: str = Field(default_factory=str)
    isDir: bool = False
    isVideo: bool = False
    type: str = "music"
    albumId: str = Field(default_factory=str)
    album: str = ""
    artistId: str = Field(default_factory=str)
    artist: str = ""
    coverArt: Optional[str] = None
    duration: float = 0
    bitRate: int = 0
    bitDepth: int = 16
    samplingRate: int = 44100
    channelCount: int = 2
    userRating: int = 0
    averageRating: float = 0.0
    track: int = 1
    year: str = ""
    genre: str = ""
    size: int = 0
    discNumber: int = 1
    suffix: str = Field(default_factory=str)
    contentType: str = "audio/mpeg"
    path: str = Field(default_factory=str)

class SubsonicAuthParams(BaseModel):
    u: Optional[str] = Query(None)
    p: Optional[str] = Query(None)
    t: Optional[str] = Query(None)
    s: Optional[str] = Query(None)
    apiKey: Optional[str] = Query(None)

def authenticate_user(
    u: str = Query(None),
    p: str = Query(None),
    session: Session = Depends(db.get_session),
) -> db.User:
    user = session.exec(select(db.User).where(db.User.login == u)).first()
    if not user or user.password != hash_password(p):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return user

def hash_password(password: str, salt: bytes = b"static_salt") -> str:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )
    return base64.b64encode(kdf.derive(password.encode())).decode()


@open_subsonic_router.get("/ping")
async def ping():
    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getPlaylists")
async def get_playlists(session: Session = Depends(db.get_session)):
    rsp = SubsonicResponse()

    playlists = session.exec(select(db.Playlist)).all()

    playlist_data = [
        {
            "id": playlist.id,
            "name": playlist.name,
            "owner": playlist.user_id,
            "songCount": playlist.total_tracks,
            "createDate": playlist.create_date,
        }
        for playlist in playlists
    ]

    rsp.data["playlists"] = {"playlist": playlist_data}

    return rsp.to_json_rsp()


@open_subsonic_router.get("/scroble")
def scroble(id: int, session: Session = Depends(db.get_session)):
    track = session.exec(select(db.Track).where(db.Track.id == id)).first()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    track.plays_count += 1
    session.add(track)
    session.commit()

    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getSongsByGenre")
def get_songs_by_genre(genre: str, session: Session = Depends(db.get_session)):
    rsp = SubsonicResponse()
    service = service_layer.TrackService(session)
    tracks = service.get_songs_by_genre(genre)
    rsp.data["songsByGenre"] = {"song": tracks}
    return rsp.to_json_rsp()


@open_subsonic_router.get("/download")
async def download(id: int, session: Session = Depends(db.get_session)):
    track = session.exec(select(db.Track).where(db.Track.id == id)).first()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    return FileResponse(track.file_path)


@open_subsonic_router.get("/stream")
async def stream(id: int, session: Session = Depends(db.get_session)):
    track = session.exec(select(db.Track).where(db.Track.id == id)).first()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    return FileResponse(track.file_path)


@open_subsonic_router.get("/search2")
async def search2(
    query: str = Query(),
    artistCount: int = Query(default=20),
    artistOffset: int = Query(default=0),
    albumCount: int = Query(default=20),
    albumOffset: int = Query(default=0),
    songCount: int = Query(default=20),
    songOffset: int = Query(default=0),
    session: Session = Depends(db.get_session),
):
    service = service_layer.SearchService(session)
    result = service.search2(
        query, artistCount, artistOffset, albumCount, albumOffset, songCount, songOffset
    )
    rsp = SubsonicResponse()
    rsp.data["searchResult2"] = result

    return rsp.to_json_rsp()


@open_subsonic_router.get("/search3")
async def search3(
    query: str = Query(),
    artistCount: int = Query(default=20),
    artistOffset: int = Query(default=0),
    albumCount: int = Query(default=20),
    albumOffset: int = Query(default=0),
    songCount: int = Query(default=20),
    songOffset: int = Query(default=0),
    session: Session = Depends(db.get_session),
):
    service = service_layer.SearchService(session)
    result = service.search3(
        query, artistCount, artistOffset, albumCount, albumOffset, songCount, songOffset
    )
    rsp = SubsonicResponse()
    rsp.data["searchResult3"] = result

    return rsp.to_json_rsp()


@open_subsonic_router.get("/getGenres")
async def get_genres(session: Session = Depends(db.get_session)):
    service = service_layer.GenreService(session)
    genres_result = service.get_genres()
    rsp = SubsonicResponse()
    rsp.data["genres"] = genres_result

    return rsp.to_json_rsp()


@open_subsonic_router.get("/getSong")
def get_song(id: int, session: Session = Depends(db.get_session)):
    service = service_layer.TrackService(session)
    track = service.get_song_by_id(id)
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    rsp = SubsonicResponse()
    rsp.data["song"] = track
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getRandomSongs")
def get_random_songs(
    size: int = 10,
    genre: Optional[str] = None,
    fromYear: Optional[str] = None,
    toYear: Optional[str] = None,
    session: Session = Depends(db.get_session),
):
    service = service_layer.TrackService(session)
    tracks = service.get_random_songs(size, genre, fromYear, toYear)
    if tracks is None:
        return JSONResponse({"detail": "No page found"}, status_code=404)

    rsp = SubsonicResponse()
    rsp.data["randomSongs"] = {"song": tracks}
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getArtist")
def get_artist(id: int, session: Session = Depends(db.get_session)):
    service = service_layer.ArtistService(session)
    artist = service.get_artist_by_id(id)
    if artist is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    rsp = SubsonicResponse()
    rsp.data["artist"] = artist
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getAlbum")
def get_album(id: int, session: Session = Depends(db.get_session)):
    service = service_layer.AlbumService(session)
    album = service.get_album_by_id(id)
    if album is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    rsp = SubsonicResponse()
    rsp.data["album"] = album
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getIndexes")
def get_indexes(
    musicFolderId: str = Query(default=""),
    ifModifiedSince: int = Query(default=0),
    session: Session = Depends(db.get_session),
):
    index_service = service_layer.IndexService(session)

    indexes = index_service.get_indexes_artists(
        musicFolderId, ifModifiedSince, with_childs=True
    )

    rsp = SubsonicResponse()
    rsp.data["indexes"] = indexes
    rsp.data["indexes"]["ignoredArticles"] = ""
    rsp.data["indexes"]["lastModified"] = 0
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getArtists")
def get_artists(
    musicFolderId: str = Query(default=""),
    session: Session = Depends(db.get_session),
):
    index_service = service_layer.IndexService(session)

    indexes = index_service.get_indexes_artists(musicFolderId)

    rsp = SubsonicResponse()
    rsp.data["artists"] = indexes
    rsp.data["artists"]["ignoredArticles"] = ""
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getUser")
async def get_user(
    username: str = Query(..., description="Имя пользователя"),
    current_user: db.User = Depends(authenticate_user),
):
    rsp = SubsonicResponse()
    if current_user.login != username:
        rsp.set_error(70, "The requested data was not found")
        return rsp.to_json_rsp()
    
    rsp.data["user"] = {
        "username": current_user.login
    }
    return rsp.to_json_rsp()