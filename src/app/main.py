from fastapi import FastAPI
from .database import init_db
from .db_endpoints import router
from .open_subsonic_api import open_subsonic_router
from .registration import registration_router

app = FastAPI()

init_db()

app.include_router(router)

app.include_router(open_subsonic_router)

app.include_router(registration_router)