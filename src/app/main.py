import asyncio
from fastapi.responses import JSONResponse
from starlette.requests import Request
from sqlmodel import Session, select
from . import database as db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .open_subsonic_api import open_subsonic_router
from .db_loading import scan_and_load
from .frontend_endpoints import frontend_router
app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scan_and_load()

app.include_router(open_subsonic_router)

app.include_router(frontend_router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    session: Session = db.get_session().__next__()
    login = request.query_params.get("u")
    password = request.query_params.get("p")
    user = session.exec(select(db.User).where((db.User.login == login) & (db.User.password == password))).one_or_none()
    if user is None:
        return JSONResponse({"detail": "Invalid login or password"}, status_code=401)
    response = await call_next(request)
    return response