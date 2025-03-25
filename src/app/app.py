from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.open_subsonic_api import open_subsonic_router
from src.app.frontend_endpoints import frontend_router
from src.app.auth import auth_router


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

app.include_router(open_subsonic_router)
app.include_router(frontend_router)
app.include_router(auth_router)
