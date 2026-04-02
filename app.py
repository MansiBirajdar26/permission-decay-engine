from flask import Flask, render_template, request, redirect, url_for
from database.db_manager import get_events, update_event_status, init_db, get_total_count
from stream_processor import start_stream
import threading

app = Flask(__name__)

# ---------------- INIT ----------------
init_db()

# ---------------- START BACKGROUND STREAM ----------------
threading.Thread(target=start_stream, daemon=True).start()


# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():
    # 1. Capture Filter Parameters from the URL
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")
    severity = request.args.get("severity", "")
    limit = 50

    # 2. Fetch filtered results (Update your db_manager functions to accept these!)
    events = get_events(page=page, limit=limit, search=search_query, severity=severity)
    total = get_total_count(search=search_query, severity=severity)

    # 3. Calculate Total Pages based on filtered total
    total_pages = (total // limit) + (1 if total % limit != 0 else 0)

    return render_template(
        "dashboard.html",
        events=events,
        page=page,
        total=total,
        total_pages=total_pages,
        search_query=search_query,  # Keep search text in the input box
        severity=severity           # Keep the dropdown selection synced
    )


# ---------------- REVOKE ----------------
@app.route("/revoke/<int:event_id>", methods=['POST', 'GET'])
def revoke(event_id):
    update_event_status(event_id, "REVOKED")
    # Redirect back to the dashboard (use url_for for better reliability)
    return redirect(url_for('dashboard'))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)