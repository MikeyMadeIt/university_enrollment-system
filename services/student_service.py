"""Student operations backed by the original StudentDictionary implementation."""

from algorithms.searching import linear_search_by_id, linear_search_by_name
from data_structures.student_dictionary import StudentDictionary


class StudentService:
    def __init__(self, storage):
        self.storage = storage
        self.students = StudentDictionary()
        for row in storage.load("students.json", []):
            if not isinstance(row, dict):
                continue
            raw_sid = row.get("student_id", row.get("id"))
            name = row.get("name", "")
            sid = str(raw_sid).strip().upper() if raw_sid is not None else ""
            if sid and isinstance(name, str) and name.strip() and self.students.add_student(
                    sid, name.strip()):
                student = self.students.get_student(sid)
                email = row.get("email", "")
                student["email"] = email.strip() if isinstance(email, str) else ""
                completed = row.get("completed_courses", [])
                if not isinstance(completed, (list, tuple, set)):
                    completed = []
                for code in completed:
                    code = str(code).strip().upper()
                    if code:
                        self.students.add_completed_course(sid, code)

    def add(self, student_id, name, email="", completed=None):
        sid, name = (student_id or "").strip().upper(), (name or "").strip()
        if not sid or not name:
            raise ValueError("Student ID and name are required")
        if not self.students.add_student(sid, name):
            raise ValueError(f"Student ID {sid} already exists")
        self.students.get_student(sid)["email"] = (email or "").strip()
        for code in completed or []:
            if code and str(code).strip():
                self.students.add_completed_course(sid, str(code).strip().upper())
        self._persist()
        return self.get(sid)

    def add_completed_course(self, student_id, course_code):
        sid = (student_id or "").strip().upper()
        code = (course_code or "").strip().upper()
        if not sid or not code:
            raise ValueError("Student ID and course code are required")
        if not self.students.add_completed_course(sid, code):
            raise ValueError(f"Student {sid} not found")
        self._persist()

    def remove(self, student_id):
        sid = (student_id or "").strip().upper()
        if not self.students.delete_student(sid):
            raise ValueError(f"Student {sid} not found")
        self._persist()

    def get(self, student_id):
        sid = (student_id or "").strip().upper()
        row = self.students.get_student(sid)
        if row is None:
            return None
        return {"student_id": sid, "name": row["name"], "email": row.get("email", ""),
                "completed_courses": list(row["completed_courses"])}

    def all(self):
        return [self.get(sid) for sid in self.students.get_all_student()]

    def search(self, query):
        query = (query or "").strip()
        if not query:
            return None
        record = linear_search_by_id(self.students.get_all_student(), query.upper())
        if record is not None:
            return self.get(query)
        return linear_search_by_name(self.all(), query)

    def _persist(self):
        self.storage.save("students.json", self.all())
