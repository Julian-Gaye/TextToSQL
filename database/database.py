import sqlite3
from config import DB_DIR, DB_PATH

def get_connection(in_memory: bool = False) -> sqlite3.Connection:
    target = ":memory:" if in_memory else DB_PATH
    conn = sqlite3.connect(target, check_same_thread=False)

    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()

    schema_file = DB_DIR / "schema.sql"
    if schema_file.exists():
        with open(schema_file, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    seed_file = DB_DIR / "data.sql"
    if seed_file.exists():
        with open(seed_file, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())

    conn.commit()
    return conn


db_conn = get_connection(in_memory=False)