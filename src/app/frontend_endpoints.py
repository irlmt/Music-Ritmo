from src.app.open_subsonic_api import SubsonicResponse, hash_password
import database as db

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import Session, select
import python_avatars as pa  # type: ignore
import base64

frontend_router = APIRouter()


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

@frontend_router.get("/authenticate")
def authenticate_user(
    u: str = Query(None),
    p: str = Query(None),
    t: str = Query(None),
    s: str = Query(None),
    k: str = Query(None),
    session: Session = Depends(db.get_session)
):
    rsp = SubsonicResponse()

    if k and (u or p or t or s):
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 43, "message": "Multiple conflicting authentication mechanisms provided"}
        return rsp.to_json_rsp()

    if (p and t) or (p and s) or (t and not s) or (s and not t):
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 43, "message": "Multiple conflicting authentication mechanisms provided"}
        return rsp.to_json_rsp()

    if k:
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 42, "message": "API key authentication not implemented"}
        return rsp.to_json_rsp()

    user = session.exec(select(db.User).where(db.User.login == u)).first()
    if not user:
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 40, "message": "Invalid credentials"}
        return rsp.to_json_rsp()

    if t and s:
        if t != hash_password(user.password, s.encode()):
            rsp.data["status"] = "failed"
            rsp.data["error"] = {"code": 40, "message": "Invalid credentials"}
            return rsp.to_json_rsp()
    elif p:
        if hash_password(p) != user.password:
            rsp.data["status"] = "failed"
            rsp.data["error"] = {"code": 40, "message": "Invalid credentials"}
            return rsp.to_json_rsp()
    else:
        rsp.data["status"] = "failed"
        rsp.data["error"] = {"code": 10, "message": "Required parameter is missing"}
        return rsp.to_json_rsp()
    
    rsp.data["user"] = {"username": user.login}
    return rsp.to_json_rsp()