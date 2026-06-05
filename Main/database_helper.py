# Main/database_helper.py
import os
import sys
import shutil
import sqlite3

def resource_path(rel_path):
    """Return path to a bundled resource or local file (works in dev and with PyInstaller)."""
    if getattr(sys, "frozen", False):
        # When using --onedir, files are located next to the exe; when using --onefile,
        # they are extracted to _MEIPASS.
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

def ensure_writable_db(bundled_db_relative, app_name="BrainTech"):
    """
    Ensure a writable DB for the user.
    - bundled_db_relative: e.g. "Database\\medical_database.db" (relative inside bundle)
    - returns path to the writable DB file (in LOCALAPPDATA)
    """
    local_appdata = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
    app_dir = os.path.join(local_appdata, app_name)
    os.makedirs(app_dir, exist_ok=True)

    user_db_path = os.path.join(app_dir, os.path.basename(bundled_db_relative))
    if not os.path.exists(user_db_path):
        # copy bundled DB to user's folder (if bundled DB exists)
        bundled_db_path = resource_path(bundled_db_relative)
        if os.path.exists(bundled_db_path):
            try:
                shutil.copy2(bundled_db_path, user_db_path)
            except Exception:
                # fallback: create empty DB if copy fails
                conn = sqlite3.connect(user_db_path)
                conn.close()
        else:
            # no bundled DB - create empty DB
            conn = sqlite3.connect(user_db_path)
            conn.close()
    return user_db_path

# Example usage:
# db_path = ensure_writable_db("Database\\medical_database.db")
# conn = sqlite3.connect(db_path)
