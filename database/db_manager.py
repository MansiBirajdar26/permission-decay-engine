import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "events.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # This allows accessing columns by name if needed
    return conn

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
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- UPDATED: GET EVENTS WITH GLOBAL FILTERING ---
def get_events(page=1, limit=50, search="", severity=""):
    conn = get_conn()
    cursor = conn.cursor()
    offset = (page - 1) * limit

    # Base Query
    query = "SELECT id, user, action, resource, timestamp, severity, score, flags, status FROM events WHERE 1=1"
    params = []

    # Add Search Filter (Searches Identity/User or Resource)
    if search:
        query += " AND (user LIKE ? OR resource LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    # Add Severity Filter
    if severity:
        query += " AND severity = ?"
        params.append(severity)

    # Order and Paginate
    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- UPDATED: GET TOTAL COUNT WITH GLOBAL FILTERING ---
def get_total_count(search="", severity=""):
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
        (user, action, resource, timestamp, score, severity, flags, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event["user"],
        event["action"],
        event["resource"],
        event["timestamp"],
        event["score"],
        event["severity"],
        event["flags"],
        event.get("status", "ALLOWED")
    ))
    conn.commit()
    conn.close()