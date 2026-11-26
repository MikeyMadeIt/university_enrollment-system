"""Course CRUD service."""


class CourseService:
    def __init__(self, storage, collection):
        self.storage = storage
        self.collection = collection

    def add(self, code, title, capacity, prerequisites=None):
        code = (code or "").strip().upper()
        title = (title or "").strip()
        if not code or not title:
            raise ValueError("Course code and title are required")
        try:
            cap = int(capacity)
        except (TypeError, ValueError):
            raise ValueError("Capacity must be an integer")
        if cap <= 0:
            raise ValueError("Capacity must be positive")

        prereqs = [p.strip().upper() for p in (prerequisites or []) if p and p.strip()]
        if code in prereqs:
            raise ValueError("A course cannot be its own prerequisite")
        for p in prereqs:
            if self.collection.get(p) is None:
                raise ValueError(f"Prerequisite course {p} does not exist")

        course = {
            "course_code": code,
            "title": title,
            "capacity": cap,
            "prerequisites": prereqs,
        }
        self.collection.add(course)
        self._persist()
        return course

    def remove(self, code):
        if not self.collection.remove(code):
            raise ValueError(f"Course {code} not found")
        self._persist()

    def get(self, code):
        return self.collection.get(code)

    def all(self):
        return self.collection.all()

    def _persist(self):
        self.storage.save("courses.json", self.collection.all())