from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from . import database as db
from fastapi.responses import RedirectResponse
import httpx

registration_router = APIRouter()

class RegisterRequest(BaseModel):
    login: str = Field(..., min_length=5, max_length=64)
    password: str = Field(..., min_length=5, max_length=64)

@registration_router.post("/registration/")
async def signup(
    register_data: RegisterRequest,
    session: Session = Depends(db.get_session)
):
    login = register_data.login
    password = register_data.password

    statement = select(db.User).where(db.User.login == login)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    async with httpx.AsyncClient() as client:
        avatar_response = await client.get("http://localhost:8000/generate_avatar/")
        if avatar_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error generating avatar")
        
        avatar_base64 = avatar_response.json().get("avatar_base64")
    
    new_user = db.User(
        login=login,
        password=password,
        avatar=avatar_base64
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return RedirectResponse(url="/", status_code=303)