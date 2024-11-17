from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .database import create_connection

router = APIRouter()


class HelloWorldMessage(BaseModel):
    message: str


@router.get("/hello")
def read_hello():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT message FROM hello_world ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {"message": "Hello, World!"}

    return {"message": row[0]}


@router.post("/hello")
def create_hello(message: HelloWorldMessage):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO hello_world (message) VALUES (?);", (message.message,))
    conn.commit()
    conn.close()

    return {"message": message.message}
