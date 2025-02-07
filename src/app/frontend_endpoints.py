import base64

import python_avatars as pa  # type: ignore
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session

from src.app.subsonic_response import SubsonicResponse

from . import database as db
from . import service_layer

frontend_router = APIRouter(prefix='/specific')


@frontend_router.get("/generate_avatar/")
def generate_random_avatar():
    try:
        avatar = pa.Avatar.random()
        svg_data = avatar.render()
        base64_avatar = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")

        return {"avatar_base64": base64_avatar}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating avatar: {str(e)}"
        )


@frontend_router.get("/getSortedArtistAlbums")
def get_sorted_artist_albums(
    id: int,
    size: int = 10,
    offset: int = 0,
    session: Session = Depends(db.get_session),
):
    album_service = service_layer.AlbumService(session)
    sortedAlbums = album_service.get_sorted_artist_albums(id, size, offset)

    rsp = SubsonicResponse()
    rsp.data["sortedAlbums"] = sortedAlbums
    return rsp.to_json_rsp()
