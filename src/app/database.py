import sqlite3
from sqlite3 import Error

DATABASE_URL = "test.db"


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_URL)
        return conn
    except Error as e:
        print(e)
    return conn


def init_db():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hello_world (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL
            );
        """)
        conn.commit()
        conn.close()
