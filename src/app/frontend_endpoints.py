from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, Response
from sqlmodel import Session, select

from src.app.subsonic_response import SubsonicResponse
from src.app.auth import authenticate_user

from . import database as db
from . import service_layer

frontend_router = APIRouter(prefix="/specific")


@frontend_router.get("/generateAvatar")
def generate_random_avatar(
    current_user: db.User = Depends(authenticate_user),
    session: Session = Depends(db.get_session)):

    avatar = service_layer.generate_and_save_avatar(session, current_user)

    return Response(content=avatar, media_type="image/png")


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
