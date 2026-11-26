"""Student operations backed by the original StudentDictionary implementation."""

from algorithms.searching import linear_search_by_id, linear_search_by_name
from data_structures.student_dictionary import StudentDictionary


class StudentService:
    def __init__(self, storage):
        self.storage = storage
        self.students = StudentDictionary()
        for row in storage.load("students.json", []):
            sid = row.get("student_id", row.get("id"))
            name = row.get("name", "")
            if sid and name and self.students.add_student(str(sid).upper(), name):
                student = self.students.get_student(str(sid).upper())
                student["email"] = row.get("email", "")
                for code in row.get("completed_courses", []):
                    self.students.add_completed_course(str(sid).upper(), str(code).upper())

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
        sid, code = student_id.strip().upper(), course_code.strip().upper()
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
