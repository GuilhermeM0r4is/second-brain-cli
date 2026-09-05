import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "sbrain.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    ''' creates the connection to the database, and the file if
     it doesn't yet exist as a first time usage '''

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    ''' creates the tables on startup, and seeds the settings row if missing '''

    conn = get_connection()

    with open(SCHEMA_PATH, "r") as file:
        schema = file.read()

    conn.executescript(schema)

    # ensure exactly one settings row exists — only insert if the table is empty
    existing = conn.execute("SELECT id FROM settings").fetchone()
    if existing is None:
        conn.execute("INSERT INTO settings DEFAULT VALUES")

    conn.commit()
    conn.close()