from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
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


@open_subsonic_router.get("/ping")
async def ping():
    rsp = SubsonicResponse()
    return rsp.to_json_rsp()


@open_subsonic_router.get("/genres/{genre_name}/tracks")
def get_tracks_by_genre(genre_name: str, session: Session = Depends(db.get_session)):
    genre = session.exec(select(db.Genre).where(db.Genre.name == genre_name)).one_or_none()
    response = SubsonicResponse()
    tracks_data = []
    for track in genre.tracks:
        track_info = {key: value for key, value in vars(track).items() if not key.startswith('_')}
        tracks_data.append(track_info)
    response.data["tracks"] = {"track": tracks_data}
    return response.to_json_rsp()
