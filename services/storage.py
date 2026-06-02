"""
Storage Service
---------------
Handles reading / writing the JSON data file that persists extracted profiles.
"""

import json
import os

# Resolve data file path relative to project root (one level up from services/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(_PROJECT_ROOT, "extracted_data.json")


def load_data():
    """Load all extracted entries from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_data(data):
    """Overwrite the JSON file with the given list of entries."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def append_entry(entry):
    """Append a single entry and return (all_data, total_count)."""
    all_data = load_data()
    all_data.append(entry)
    save_data(all_data)
    return all_data, len(all_data)


def delete_entry(index):
    """
    Delete entry at *index*.
    Returns (deleted_entry, remaining_count) on success, or None on failure.
    """
    all_data = load_data()
    if 0 <= index < len(all_data):
        deleted = all_data.pop(index)
        save_data(all_data)
        return deleted, len(all_data)
    return None


def clear_all():
    """Remove every entry."""
    save_data([])
