import sqlite3
from contextlib import closing

DB_NAME = "checkerdata.db"  # don't change unless you change it everywhere


def init_db(db_path: str = DB_NAME) -> None:
    """Create database + tables safely (works on Railway too)."""
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")  # better reliability
        conn.execute("PRAGMA foreign_keys=ON;")

        conn.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            state   TEXT DEFAULT '',
            post    TEXT DEFAULT ''
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS Groups (
            chat_id INTEGER PRIMARY KEY,
            link    TEXT DEFAULT ''
        )
        """)

        conn.commit()


def upsert_group(chat_id: int, link: str, db_path: str = DB_NAME) -> None:
    """Insert group if not exists, otherwise update link."""
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("""
        INSERT INTO Groups (chat_id, link)
        VALUES (?, ?)
        ON CONFLICT(chat_id) DO UPDATE SET link=excluded.link
        """, (chat_id, link))
        conn.commit()


def get_groups(db_path: str = DB_NAME):
    with closing(sqlite3.connect(db_path)) as conn:
        cur = conn.execute("SELECT chat_id, link FROM Groups")
        return cur.fetchall()


def ensure_user(user_id: int, db_path: str = DB_NAME) -> None:
    """Make sure user row exists."""
    with closing(sqlite3.connect(db_path)) as conn:
        conn.execute("INSERT OR IGNORE INTO Users (user_id) VALUES (?)", (user_id,))
        conn.commit()