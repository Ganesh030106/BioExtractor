"""
API Routes
----------
All REST endpoints are registered as a Flask Blueprint so they can be
imported into the main app without circular dependencies.

Extraction priority:
  1. Google Gemini AI  (if API key is configured)
  2. Regex-based fallback  (if Gemini fails or is not configured)
"""

from flask import Blueprint, request, jsonify

from config.settings import is_gemini_configured
from services.gemini_service import extract_with_gemini
from services.extractor import extract_info as extract_info_regex
from services.storage import load_data, append_entry, delete_entry, clear_all

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ------------------------------------------------------------------ #
#  Unified extraction (Gemini → regex fallback)
# ------------------------------------------------------------------ #
def _extract(text, api_key=None):
    """Try Gemini first; fall back to regex on failure."""
    result = extract_with_gemini(text, api_key=api_key)
    if result is not None:
        return result

    # Regex fallback
    extracted = extract_info_regex(text)
    extracted["extracted_by"] = "regex"
    return extracted


# ------------------------------------------------------------------ #
#  GET  /api/status  — Check Gemini configuration
# ------------------------------------------------------------------ #
@api_bp.route("/status", methods=["GET"])
def status():
    """Return whether Gemini AI is configured."""
    configured = is_gemini_configured()
    return jsonify({
        "gemini_configured": configured,
        "extraction_engine": "gemini" if configured else "regex",
    })


# ------------------------------------------------------------------ #
#  POST  /api/extract
# ------------------------------------------------------------------ #
@api_bp.route("/extract", methods=["POST"])
def extract():
    """Extract structured information from submitted text."""
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "Empty text provided"}), 400

    # Extract API key from the X-Gemini-API-Key request header
    api_key = request.headers.get("X-Gemini-API-Key")

    extracted = _extract(text, api_key=api_key)
    _, total = append_entry(extracted)

    return jsonify({
        "success": True,
        "extracted": extracted,
        "total_entries": total,
    })


# ------------------------------------------------------------------ #
#  GET  /api/history
# ------------------------------------------------------------------ #
@api_bp.route("/history", methods=["GET"])
def history():
    """Return every extracted profile."""
    all_data = load_data()
    return jsonify({
        "entries": all_data,
        "total": len(all_data),
    })


# ------------------------------------------------------------------ #
#  DELETE  /api/delete/<index>
# ------------------------------------------------------------------ #
@api_bp.route("/delete/<int:index>", methods=["DELETE"])
def delete(index):
    """Delete a single entry by its list index."""
    result = delete_entry(index)
    if result is None:
        return jsonify({"error": "Invalid index"}), 404

    deleted, remaining = result
    return jsonify({
        "success": True,
        "deleted": deleted,
        "total_entries": remaining,
    })


# ------------------------------------------------------------------ #
#  DELETE  /api/clear
# ------------------------------------------------------------------ #
@api_bp.route("/clear", methods=["DELETE"])
def clear():
    """Delete all entries."""
    clear_all()
    return jsonify({"success": True, "message": "All data cleared"})


# ------------------------------------------------------------------ #
#  GET  /api/export
# ------------------------------------------------------------------ #
@api_bp.route("/export", methods=["GET"])
def export_data():
    """Return all entries as a downloadable JSON attachment."""
    all_data = load_data()
    return (
        jsonify(all_data),
        200,
        {"Content-Disposition": "attachment; filename=extracted_profiles.json"},
    )
