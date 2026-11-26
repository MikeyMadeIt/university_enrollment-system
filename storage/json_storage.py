
"""JSON file persistence for the enrollment system."""

import json
import os


class JsonStorage:
    """Simple read/write wrapper around JSON files in a base directory."""

    def __init__(self, base_dir="data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _path(self, filename):
        return os.path.join(self.base_dir, filename)

    def load(self, filename, default=None):
        """Load JSON list/dict. Returns `default` (or []) if missing/corrupt."""
        path = self._path(filename)
        fallback = [] if default is None else default
        if not os.path.exists(path):
            return fallback
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return fallback

    def save(self, filename, data):
        path = self._path(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)