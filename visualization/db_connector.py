"""Open a MySQL connection using the repository's local credentials."""

import json
from pathlib import Path

import mysql.connector


def get_connection():
    """Connect using config/db.json without storing credentials in code."""
    config_path = Path(__file__).resolve().parent.parent / "config" / "db.json"
    with config_path.open(encoding="utf-8") as file:
        settings = json.load(file)
    return mysql.connector.connect(**settings)
