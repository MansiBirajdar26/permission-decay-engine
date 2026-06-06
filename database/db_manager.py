import sqlite3
import os

DB_PATH = "database/events.db"


def get_conn():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # returns dict-like rows
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user TEXT,
        action TEXT,
        resource TEXT,
        score INTEGER,
        status TEXT,
        severity TEXT,
        flags TEXT,
        days_unused INTEGER
    )
    """)

    conn.commit()
    conn.close()


def insert_event(event):
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    INSERT INTO events (
        timestamp, user, action, resource,
        score, status, severity, flags, days_unused
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("timestamp"),
        event.get("user"),
        event.get("action"),
        event.get("resource"),
        event.get("score"),
        event.get("status"),
        event.get("severity"),
        event.get("flags"),
        event.get("days_unused")
    ))

    conn.commit()
    conn.close()


def get_events_paginated(page, per_page):
    conn = get_conn()
    c = conn.cursor()

    offset = (page - 1) * per_page

    c.execute("SELECT COUNT(*) FROM events")
    total = c.fetchone()[0]

    total_pages = max(1, (total + per_page - 1) // per_page)

    c.execute("""
    SELECT * FROM events
    ORDER BY id DESC
    LIMIT ? OFFSET ?
    """, (per_page, offset))

    rows = c.fetchall()
    conn.close()

    # Convert Row objects → plain dicts so jsonify() can serialize them
    return [dict(row) for row in rows], total_pages