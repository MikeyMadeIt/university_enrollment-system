"""Student CRUD service."""


class StudentService:
    def __init__(self, storage, collection):
        self.storage = storage
        self.collection = collection

    def add(self, student_id, name, email, completed=None):
        sid = (student_id or "").strip().upper()
        name = (name or "").strip()
        if not sid or not name:
            raise ValueError("Student ID and name are required")
        completed = [c.strip().upper() for c in (completed or []) if c and c.strip()]
        student = {
            "student_id": sid,
            "name": name,
            "email": (email or "").strip(),
            "completed_courses": completed,
        }
        self.collection.add(student)
        self._persist()
        return student

    def remove(self, student_id):
        if not self.collection.remove(student_id):
            raise ValueError(f"Student {student_id} not found")
        self._persist()

    def get(self, student_id):
        return self.collection.get(student_id)

    def all(self):
        return self.collection.all()

    def _persist(self):
        self.storage.save("students.json", self.collection.all())