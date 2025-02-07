import base64
import python_avatars as pa  # type: ignore
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from sqlmodel import Session, select

from src.app.subsonic_response import SubsonicResponse

from . import database as db
from . import service_layer

frontend_router = APIRouter(prefix="/specific")


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


@frontend_router.get("/getCoverArtPreview")
def get_cover_art_preview(id: int, session: Session = Depends(db.get_session)):
    track = session.exec(select(db.Track).where(db.Track.id == id)).one_or_none()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    return Response(content=track.cover, media_type=f"image/{track.cover_type}")
