from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse, Response
from sqlmodel import Session, select
import python_avatars as pa
import base64

from . import database as db

frontend_router = APIRouter()

@frontend_router.get("/generate_avatar/")
def generate_random_avatar():
    try:
        avatar = pa.Avatar.random()
        svg_data = avatar.render()
        base64_avatar = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")

        return {"avatar_base64": base64_avatar}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating avatar: {str(e)}")
    
@frontend_router.get("/getCoverArtPreview")
def getCoverArtPreview(id: int, session: Session = Depends(db.get_session)):
    track = session.exec(select(db.Track).where(db.Track.id == id)).one_or_none()
    if track is None:
        return JSONResponse({"detail": "No such id"}, status_code=404)

    return Response(content=track.cover, media_type=track.cover_type)
