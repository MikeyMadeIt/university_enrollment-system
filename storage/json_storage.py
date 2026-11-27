import json
from pathlib import Path

class JsonStorage:
    """Handles loading and saving JSON files."""

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, filename):
        return self.data_dir / filename

    def load(self, filename, default=None):
        path = self._path(filename)
        if not path.exists():
            return default if default is not None else {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            return default if default is not None else {}

        # Callers choose a default with the expected root type (dict or list).
        # Treat a valid JSON document with the wrong shape like corrupt data.
        if default is not None and not isinstance(data, type(default)):
            return default
        return data

    def save(self, filename, data):
        path = self._path(filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # Convenience helpers -------------------------------------------------
    def load_students(self):
        return self.load("students.json", {})

    def save_students(self, students):
        self.save("students.json", students)

    def load_courses(self):
        return self.load("courses.json", {})

    def save_courses(self, courses):
        self.save("courses.json", courses)

    def load_enrollments(self):
        return self.load("enrollments.json", [])

    def save_enrollments(self, enrollments):
        self.save("enrollments.json", enrollments)
