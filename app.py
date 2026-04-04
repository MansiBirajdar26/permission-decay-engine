from flask import Flask, render_template, request, redirect, url_for
from database.db_manager import get_events, update_event_status, init_db, get_total_count
from stream_processor import start_stream
import threading

app = Flask(__name__)

# ---------------- INIT ----------------
init_db()

# ---------------- START BACKGROUND STREAM ----------------
# This keeps your log processing running in a separate thread
threading.Thread(target=start_stream, daemon=True).start()


# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():
    # 1. Get filter parameters from the URL
    page = request.args.get("page", 1, type=int)
    search_query = request.args.get("search", "")
    severity = request.args.get("severity", "")
    time_filter = request.args.get("time_filter", "all")
    
    limit = 50 # Showing maximum logs per page as requested

    # 2. Fetch filtered events from DB
    # Ensure your get_events function in db_manager.py accepts these 4 arguments
    events = get_events(
        page=page, 
        limit=limit, 
        search=search_query, 
        severity=severity,
        time_filter=time_filter
    )

    # 3. Get total count of FILTERED events for correct pagination
    total = get_total_count(
        search=search_query, 
        severity=severity,
        time_filter=time_filter
    )

    # 4. Calculate total pages
    total_pages = (total // limit) + (1 if total % limit != 0 else 0)

    return render_template(
        "dashboard.html",
        events=events,
        page=page,
        total=total,
        total_pages=total_pages,
        search_query=search_query,
        severity=severity,
        time_filter=time_filter
    )


# ---------------- REVOKE ----------------
# Updated to use POST for better security, but kept GET compatible for your links
@app.route("/revoke/<int:event_id>", methods=['GET', 'POST'])
def revoke(event_id):
    update_event_status(event_id, "REVOKED")
    # Redirect back to the main dashboard
    return redirect(url_for('dashboard'))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)