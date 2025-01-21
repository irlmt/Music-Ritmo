from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, Field
from cryptography.fernet import Fernet
from . import database as db
import httpx

SECRET_KEY = Fernet.generate_key()
fernet = Fernet(SECRET_KEY)

frontend_router = APIRouter()

class RegisterRequest(BaseModel):
    login: str = Field(..., min_length=5, max_length=64)
    password: str = Field(..., min_length=5, max_length=64)

def generate_token(user_id: int) -> str:
    user_id_bytes = str(user_id).encode()
    token = fernet.encrypt(user_id_bytes)
    return token.decode()

def decode_token(token: str) -> int:
    try:
        user_id_bytes = fernet.decrypt(token.encode())
        return int(user_id_bytes.decode())
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@frontend_router.post("/registration/")
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

    token = generate_token(new_user.id)

    return {"message": "Registration successful", "token": token}
