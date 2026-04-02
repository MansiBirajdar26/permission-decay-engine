from flask import Flask, render_template, request, redirect
from database.db_manager import get_events, update_event_status, init_db, get_total_count
from stream_processor import start_stream
import threading

app = Flask(__name__)

# INIT DB
init_db()

# START STREAM
threading.Thread(target=start_stream, daemon=True).start()


@app.route("/")
def dashboard():
    page = int(request.args.get("page", 1))
    limit = 20

    events = get_events(page=page, limit=limit)
    total = get_total_count()

    total_pages = (total // limit) + (1 if total % limit != 0 else 0)

    return render_template(
        "dashboard.html",
        events=events,
        page=page,
        total=total,
        total_pages=total_pages
    )


@app.route("/revoke/<int:event_id>")
def revoke(event_id):
    update_event_status(event_id, "REVOKED")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)