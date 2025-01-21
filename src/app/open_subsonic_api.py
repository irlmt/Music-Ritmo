from typing import Optional, List

from fastapi import APIRouter, Depends
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


@open_subsonic_router.get("/genres/{genre_name}/tracks")
def get_tracks_by_genre(genre_name: str, session: Session = Depends(db.get_session)):
    rsp = SubsonicResponse()
    genre = session.exec(select(db.Genre).where(db.Genre.name == genre_name)).one_or_none()
    tracks_data = []
    for track in genre.tracks:
        track_info = SubsonicTrack(
            id=str(track.id) if hasattr(track, 'id') else SubsonicTrack.model_fields['id'].default,
            parent=str(track.parent_id) if hasattr(track, 'parent_id') else SubsonicTrack.model_fields[
                'parent'].default,
            title=track.title if hasattr(track, 'title') else SubsonicTrack.model_fields['title'].default,
            isDir=track.is_dir if hasattr(track, 'is_dir') else SubsonicTrack.model_fields['isDir'].default,
            isVideo=track.is_video if hasattr(track, 'is_video') else SubsonicTrack.model_fields['isVideo'].default,
            type=track.type if hasattr(track, 'type') else SubsonicTrack.model_fields['type'].default,
            albumId=str(track.album_id) if hasattr(track, 'album_id') else SubsonicTrack.model_fields[
                'albumId'].default,
            album=str(track.album) if hasattr(track, 'album') else SubsonicTrack.model_fields['album'].default,
            artistId=str(track.artist_id) if hasattr(track, 'artist_id') else SubsonicTrack.model_fields[
                'artistId'].default,
            artist=track.artist if hasattr(track, 'artist') else SubsonicTrack.model_fields['artist'].default,
            coverArt=track.cover_art if hasattr(track, 'cover_art') else SubsonicTrack.model_fields['coverArt'].default,
            duration=track.duration if hasattr(track, 'duration') else SubsonicTrack.model_fields['duration'].default,
            bitRate=track.bit_rate if hasattr(track, 'bit_rate') else SubsonicTrack.model_fields['bitRate'].default,
            bitDepth=track.bit_depth if hasattr(track, 'bit_depth') else SubsonicTrack.model_fields['bitDepth'].default,
            samplingRate=track.sampling_rate if hasattr(track, 'sampling_rate') else SubsonicTrack.model_fields[
                'samplingRate'].default,
            channelCount=track.channel_count if hasattr(track, 'channel_count') else SubsonicTrack.model_fields[
                'channelCount'].default,
            userRating=track.user_rating if hasattr(track, 'user_rating') else SubsonicTrack.model_fields[
                'userRating'].default,
            averageRating=track.average_rating if hasattr(track, 'average_rating') else SubsonicTrack.model_fields[
                'averageRating'].default,
            track=track.track_number if hasattr(track, 'track_number') else SubsonicTrack.model_fields['track'].default,
            year=track.year if hasattr(track, 'year') else SubsonicTrack.model_fields['year'].default,
            genre=track.genre if hasattr(track, 'genre') else SubsonicTrack.model_fields['genre'].default,
            size=track.size if hasattr(track, 'size') else SubsonicTrack.model_fields['size'].default,
            discNumber=track.disc_number if hasattr(track, 'disc_number') else SubsonicTrack.model_fields[
                'discNumber'].default,
            suffix=track.suffix if hasattr(track, 'suffix') else SubsonicTrack.model_fields['suffix'].default,
            contentType=track.content_type if hasattr(track, 'content_type') else SubsonicTrack.model_fields[
                'contentType'].default,
            path=track.path if hasattr(track, 'path') else SubsonicTrack.model_fields['path'].default
        )
        tracks_data.append(track_info.model_dump())
    rsp.data["track"] = tracks_data
    return rsp.to_json_rsp()
