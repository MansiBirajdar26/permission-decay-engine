import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "events.db")


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            action TEXT,
            resource TEXT,
            timestamp TEXT,
            score INTEGER,
            severity TEXT,
            flags TEXT,
            status TEXT,
            days_unused INTEGER
        )
    """)

    conn.commit()
    conn.close()


def insert_event(event):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events 
        (user, action, resource, timestamp, score, severity, flags, status, days_unused)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("user"),
        event.get("action"),
        event.get("resource"),
        event.get("timestamp"),
        event.get("score"),
        event.get("severity"),
        event.get("flags"),
        event.get("status", "ALLOWED"),
        event.get("days_unused", 0)
    ))

    conn.commit()
    conn.close()


def get_events(page=1, limit=20):
    conn = get_conn()
    cursor = conn.cursor()

    offset = (page - 1) * limit

    cursor.execute("""
        SELECT * FROM events
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_total_count():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def update_event_status(event_id, status):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE events SET status=? WHERE id=?
    """, (status, event_id))

    conn.commit()
    conn.close()