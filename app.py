from flask import Flask, render_template, request, jsonify, send_from_directory
from database.db_manager import get_events_paginated, init_db
from stream_processor import start_stream
import threading

app = Flask(__name__)

# ✅ FIRST: init DB
init_db()

# ✅ THEN: start stream
threading.Thread(target=start_stream, daemon=True).start()


@app.route("/")
def dashboard():
    page = int(request.args.get("page", 1))
    per_page = 50

    events, total_pages = get_events_paginated(page, per_page)

    return render_template(
        "dashboard.html",
        events=events,
        page=page,
        total_pages=total_pages
    )


# ================== 🔥 NEW API (for frontend fetch) ==================
@app.route("/api/events")
def api_events():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("limit", 50))

    events, total_pages = get_events_paginated(page, per_page)

    return jsonify({
        "events": events,
        "page": page,
        "total_pages": total_pages
    })


# ================== 🔧 OPTIONAL (fix favicon noise) ==================
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')


if __name__ == "__main__":
    app.run(debug=True)