from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
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

@open_subsonic_router.get("/getPlaylists")
async def get_playlists(session: AsyncSession = Depends(db.get_session)):
    rsp = SubsonicResponse()

    try:
        result = await session.execute(select(db.Playlist))
        playlists = result.scalars().all()

        rsp.data["playlists"] = {
            "playlist": [
                {
                    "id": playlist.id,
                    "name": playlist.name,
                    "owner": playlist.user_id,
                    "songCount": playlist.total_tracks,
                    "created": playlist.create_date,
                }
                for playlist in playlists
            ]
        }
    except Exception as e:
        rsp.data["status"] = "failed"
        rsp.data["error"] = str(e)

    return rsp.to_json_rsp()