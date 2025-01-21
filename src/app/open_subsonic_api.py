from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from . import database as db

open_subsonic_router = APIRouter(prefix="/rest")


class SubsonicResponse:
    def __init__(self):
        self.data = {}
        self.data["status"] = "ok"
        self.data["version"] = "1.16.1"
        self.data["type"] = "MusicRitmo"
        self.data["serverVersion"] = "0.1"
        self.data["openSubsonic"] = True

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
    album: Optional[str] = None
    artistId: str = Field(default_factory=str)
    artist: Optional[str] = ""
    coverArt: Optional[str] = None
    duration: float = 0
    bitRate: int = 0
    bitDepth: int = 16
    samplingRate: int = 44100
    channelCount: int = 2
    userRating: int = 0
    averageRating: float = 0.0
    track: int = 1
    year: Optional[int] = None
    genre: Optional[str] = None
    size: int = 0
    discNumber: int = 1
    suffix: str = Field(default_factory=str)
    contentType: str = "audio/mpeg"
    path: str = Field(default_factory=str)


@open_subsonic_router.get("/ping")
async def ping():
    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/getTracksByGenre")
def get_tracks_by_genre(genre: str, session: Session = Depends(db.get_session)):
    rsp = SubsonicResponse()
    genre = session.exec(select(db.Genre).where(db.Genre.name == genre)).one_or_none()
    tracks_data = []
    for track in genre.tracks:
        track_info = SubsonicTrack(
            id=str(track.id),
            parent=SubsonicTrack.model_fields['parent'].default,
            title=track.title,
            isDir=SubsonicTrack.model_fields['isDir'].default,
            isVideo=SubsonicTrack.model_fields['isVideo'].default,
            type=track.type,
            albumId=str(track.album_id),
            album=str(track.album),
            artistId=SubsonicTrack.model_fields['artistId'].default,
            artist=SubsonicTrack.model_fields['artist'].default,
            coverArt=SubsonicTrack.model_fields['coverArt'].default,
            duration=track.duration,
            bitRate=SubsonicTrack.model_fields['bitRate'].default,
            bitDepth=SubsonicTrack.model_fields['bitDepth'].default,
            samplingRate=SubsonicTrack.model_fields['samplingRate'].default,
            channelCount=SubsonicTrack.model_fields['channelCount'].default,
            userRating=SubsonicTrack.model_fields['userRating'].default,
            averageRating=SubsonicTrack.model_fields['averageRating'].default,
            track=SubsonicTrack.model_fields['track'].default,
            year=track.year,
            genre=SubsonicTrack.model_fields['genre'].default,
            size=SubsonicTrack.model_fields['size'].default,
            discNumber=SubsonicTrack.model_fields['discNumber'].default,
            suffix=SubsonicTrack.model_fields['suffix'].default,
            contentType=SubsonicTrack.model_fields['contentType'].default,
            path=track.file_path
        )
        tracks_data.append(track_info.model_dump())
    rsp.data["track"] = tracks_data
    return rsp.to_json_rsp()
