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

# --- UPDATED: GET EVENTS WITH ALL FILTERS ---
def get_events(page=1, limit=50, search="", severity="", time_filter="all"):
    conn = get_conn()
    cursor = conn.cursor()
    offset = (page - 1) * limit

    # We select columns in a specific order to match the HTML e[index] logic
    query = "SELECT id, user, action, resource, timestamp, severity, score, status FROM events WHERE 1=1"
    params = []

    # 1. Global Search (Identity or Resource)
    if search:
        query += " AND (user LIKE ? OR resource LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    # 2. Severity Filter
    if severity:
        query += " AND severity = ?"
        params.append(severity)

    # 3. Time Filter Logic
    if time_filter == "24h":
        query += " AND timestamp >= datetime('now', '-1 day')"
    elif time_filter == "7d":
        query += " AND timestamp >= datetime('now', '-7 days')"
    elif time_filter == "30d":
        query += " AND timestamp >= datetime('now', '-30 days')"

    # Order and Paginate
    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- UPDATED: GET TOTAL COUNT WITH ALL FILTERS ---
def get_total_count(search="", severity="", time_filter="all"):
    conn = get_conn()
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM events WHERE 1=1"
    params = []

    if search:
        query += " AND (user LIKE ? OR resource LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    if severity:
        query += " AND severity = ?"
        params.append(severity)

    if time_filter == "24h":
        query += " AND timestamp >= datetime('now', '-1 day')"
    elif time_filter == "7d":
        query += " AND timestamp >= datetime('now', '-7 days')"
    elif time_filter == "30d":
        query += " AND timestamp >= datetime('now', '-30 days')"

    cursor.execute(query, params)
    count = cursor.fetchone()[0]
    conn.close()
    return count

def update_event_status(event_id, status):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET status=? WHERE id=?", (status, event_id))
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