import pytest
from fastapi.testclient import TestClient
from src.app.main import app
from src.app.database import create_connection

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS hello_world;")
    cursor.execute("""
        CREATE TABLE hello_world (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def test_read_hello_empty():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_create_hello():
    response = client.post("/hello", json={"message": "Привет, мир!"})
    assert response.status_code == 200
    assert response.json() == {"message": "Привет, мир!"}


def test_read_hello_after_creation():
    client.post("/hello", json={"message": "Привет, мир!"})
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Привет, мир!"}
