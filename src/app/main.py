from fastapi import FastAPI
from .database import init_db
from .endpoints import router as hello_router

app = FastAPI()

init_db()

app.include_router(hello_router)
