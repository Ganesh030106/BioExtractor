"""
BioExtractor — Main Application Entry Point
--------------------------------------------
This file only creates the Flask app, registers blueprints,
and serves the frontend. All business logic lives in:
    • config/settings.py      → API keys & environment config
    • api/routes.py           → REST endpoints (Flask Blueprint)
    • services/gemini_service.py → Google Gemini AI extraction
    • services/extractor.py   → Regex-based fallback extraction
    • services/storage.py     → JSON file persistence
"""

from flask import Flask, render_template
from api.routes import api_bp
from config.settings import APP_PORT, DEBUG_MODE

app = Flask(__name__)

# Register the API blueprint  (/api/extract, /api/history, …)
app.register_blueprint(api_bp)


@app.route("/")
def index():
    """Serve the main frontend page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=DEBUG_MODE, port=APP_PORT)
