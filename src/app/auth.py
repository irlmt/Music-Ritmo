from fastapi import Depends, HTTPException, Query
from sqlmodel import Session, select

from . import database as db

def authenticate_user(
    u: str = Query(None),
    p: str = Query(None),
    session: Session = Depends(db.get_session),
) -> db.User:
    user = session.exec(select(db.User).where(db.User.login == u)).first()
    if not user or user.password != p:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return user
