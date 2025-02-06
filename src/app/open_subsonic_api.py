from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import hashlib

from . import database as db
from . import service_layer

open_subsonic_router = APIRouter(prefix="/rest")


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

@open_subsonic_router.get("/authenticate")
def authenticate_user(
    u: str = Query(None, alias="username"),
    p: str = Query(None, alias="password"),
    t: str = Query(None, alias="token"),
    s: str = Query(None, alias="salt"),
    apiKey: str = Query(None, alias="apiKey"),
    session: Session = Depends(db.get_session)
):
    rsp = SubsonicResponse()

    if apiKey and (u or p or t or s):
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 43, "message": "Multiple conflicting authentication mechanisms provided"}
        return rsp.to_json_rsp()

    if (p and t) or (p and s) or (t and not s) or (s and not t):
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 43, "message": "Multiple conflicting authentication mechanisms provided"}
        return rsp.to_json_rsp()

    if apiKey:
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 42, "message": "API key authentication not implemented"}
        return rsp.to_json_rsp()

    user = session.exec(select(db.User).where(db.User.login == u)).first()
    if not user:
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 40, "message": "Invalid credentials"}
        return rsp.to_json_rsp()

    if t and s:
        if t != md5_hash(user.password, s):
            rsp.data["status"] = "failed"
            rsp.data["error"] = {"code": 40, "message": "Invalid credentials"}
            return rsp.to_json_rsp()
    
    elif p:
        if not verify_password(p, user.password):
            rsp.data["status"] = "failed"
            rsp.data["error"] = {"code": 40, "message": "Invalid credentials"}
            return rsp.to_json_rsp()
    
    else:
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 10, "message": "Required parameter is missing"}
        return rsp.to_json_rsp()

    rsp.data["user"] = {"username": user.login}
    return rsp.to_json_rsp()

def md5_hash(password: str, salt: str) -> str:
    return hashlib.md5((password + salt).encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not plain_password:
        return False
    hashed_input = hashlib.pbkdf2_hmac("sha256", plain_password.encode(), b"static_salt", 100000).hex()
    return hashed_input == hashed_password