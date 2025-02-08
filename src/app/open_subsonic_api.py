from typing import Optional, List
import asyncio

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from src.app.subsonic_response import SubsonicResponse

from . import database as db
from . import service_layer
from . import db_loading
from . import utils

open_subsonic_router = APIRouter(prefix="/rest")


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
async def get_playlists(username: str = "", session: Session = Depends(db.get_session)):
    service = service_layer.PlaylistService(session)
    playlists = service.get_playlists()
    rsp = SubsonicResponse()
    rsp.data["playlists"] = playlists

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


@open_subsonic_router.get("/getPlaylist")
def get_playlist(id: int, session: Session = Depends(db.get_session)):
    service = service_layer.PlaylistService(session)
    playlist = service.get_playlist(id)
    if playlist is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)
    rsp = SubsonicResponse()
    rsp.data["playlist"] = playlist
    return rsp.to_json_rsp()


@open_subsonic_router.get("/createPlaylist")
def create_playlist(
    name: str,
    songId: List[int] = Query(default=[]),
    playlistId: int = 0,
    session: Session = Depends(db.get_session),
):
    service = service_layer.PlaylistService(session)
    playlist = service.create_playlist(name, songId)
    rsp = SubsonicResponse()
    rsp.data["playlist"] = playlist
    return rsp.to_json_rsp()


@open_subsonic_router.get("/deletePlaylist")
def delete_playlist(id: int, session: Session = Depends(db.get_session)):
    service = service_layer.PlaylistService(session)
    service.delete_playlist(id)
    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/updatePlaylist")
def update_playlist(
    playlistId: int,
    name: str = "",
    songIdToAdd: List[int] = Query(default=[]),
    songIdToRemove: List[int] = Query(default=[]),
    comment: str = "",
    public: str = "",
    session: Session = Depends(db.get_session),
):
    service = service_layer.PlaylistService(session)
    playlist = service.update_playlist(playlistId, name, songIdToAdd, songIdToRemove)
    if playlist is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)
    rsp = SubsonicResponse()
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


@open_subsonic_router.get("/star")
def star(
    id: List[int] = Query(default=[]),
    albumId: List[int] = Query(default=[]),
    artistId: List[int] = Query(default=[]),
    playlistId: List[int] = Query(default=[]),
    session: Session = Depends(db.get_session),
):
    service = service_layer.StarService(session)
    service.star(id, albumId, artistId, playlistId)
    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/unstar")
def unstar(
    id: List[int] = Query(default=[]),
    albumId: List[int] = Query(default=[]),
    artistId: List[int] = Query(default=[]),
    playlistId: List[int] = Query(default=[]),
    session: Session = Depends(db.get_session),
):
    service = service_layer.StarService(session)
    service.unstar(id, albumId, artistId, playlistId)
    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getStarred")
def get_starred(
    musicFolderId: int = 0,
    session: Session = Depends(db.get_session),
):
    service = service_layer.StarService(session)
    starred = service.get_starred()
    rsp = SubsonicResponse()
    rsp.data["starred"] = starred
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getStarred2")
def get_starred2(
    musicFolderId: int = 0,
    session: Session = Depends(db.get_session),
):
    service = service_layer.StarService(session)
    starred = service.get_starred()
    rsp = SubsonicResponse()
    rsp.data["starred2"] = starred
    return rsp.to_json_rsp()


@open_subsonic_router.get("/startScan")
async def start_scan(session: Session = Depends(db.get_session)):
    db_loading.scanStatus["scanning"] = True
    db_loading.scanStatus["count"] = 0

    utils.clear_media(session)
    asyncio.get_running_loop().run_in_executor(None, db_loading.scan_and_load)

    rsp = SubsonicResponse()
    rsp.data["scanStatus"] = db_loading.scanStatus
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getScanStatus")
def get_scan_status():
    rsp = SubsonicResponse()
    rsp.data["scanStatus"] = db_loading.scanStatus
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getAlbumList")
def get_album_list(
    type: str,
    size: int = 10,
    offset: int = 0,
    fromYear: Optional[str] = None,
    toYear: Optional[str] = None,
    genre: Optional[str] = None,
    musicFolderId: Optional[str] = None,
    session: Session = Depends(db.get_session),
):
    album_service = service_layer.AlbumService(session)

    request_type: service_layer.RequestType = service_layer.RequestType.BY_NAME
    match type:
        case "random":
            request_type = service_layer.RequestType.RANDOM
        case "alphabeticalByName":
            request_type = service_layer.RequestType.BY_NAME
        case "alphabeticalByArtist":
            request_type = service_layer.RequestType.BY_ARTIST
        case "byYear":
            request_type = service_layer.RequestType.BY_YEAR
        case "newest" | "highest" | "frequent" | "recent" | "byGenre":
            # Not implemented
            request_type = service_layer.RequestType.BY_NAME
        case _:
            return JSONResponse({"detail": "Invalid arguments"}, status_code=400)

    albums = album_service.get_album_list(
        request_type, size, offset, fromYear, toYear, genre, musicFolderId
    )
    if albums is None:
        return JSONResponse({"detail": "Invalid arguments"}, status_code=400)

    rsp = SubsonicResponse()
    rsp.data["albumList"] = albums
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getAlbumList2")
def get_album_list2(
    type: str,
    size: int = 10,
    offset: int = 0,
    fromYear: Optional[str] = None,
    toYear: Optional[str] = None,
    genre: Optional[str] = None,
    musicFolderId: Optional[str] = None,
    session: Session = Depends(db.get_session),
):
    album_service = service_layer.AlbumService(session)

    request_type: service_layer.RequestType = service_layer.RequestType.BY_NAME
    match type:
        case "random":
            request_type = service_layer.RequestType.RANDOM
        case "alphabeticalByName":
            request_type = service_layer.RequestType.BY_NAME
        case "alphabeticalByArtist":
            request_type = service_layer.RequestType.BY_ARTIST
        case "byYear":
            request_type = service_layer.RequestType.BY_YEAR
        case "newest" | "highest" | "frequent" | "recent" | "byGenre":
            # Not implemented
            request_type = service_layer.RequestType.BY_NAME
        case _:
            return JSONResponse({"detail": "Invalid arguments"}, status_code=400)

    albums = album_service.get_album_list(
        request_type, size, offset, fromYear, toYear, genre, musicFolderId
    )
    if albums is None:
        return JSONResponse({"detail": "Invalid arguments"}, status_code=400)

    rsp = SubsonicResponse()
    rsp.data["albumList2"] = albums
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getOpenSubsonicExtensions")
def get_open_subsonic_extensions():
    rsp = SubsonicResponse()
    rsp.data["openSubsonicExtensions"] = []
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getMusicFolders")
def get_music_folders():
    rsp = SubsonicResponse()
    rsp.data["musicFolders"] = {"musicFolder": [{"id": 1, "name": "tracks"}]}
    return rsp.to_json_rsp()
