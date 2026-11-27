from storage.json_storage import JsonStorage
from utils.validation import validate_student_id, validate_name
from data_structures.student_dictionary import StudentDictionary
from algorithms.searching import linear_search_by_name, linear_search_by_id
from algorithms.sorting import bubble_sort_by_name


class StudentService:
    def __init__(self, storage=None):
        self.storage = storage or JsonStorage()
        self.dict = StudentDictionary()
        self._load()

    def _load(self):
        raw = self.storage.load_students()
        for sid, info in raw.items():
            self.dict.add_student(sid, info["name"])
            for course in info.get("completed_courses", []):
                self.dict.add_completed_course(sid, course)

    def _save(self):
        raw = {}
        for sid, info in self.dict.get_all_student().items():
            raw[sid] = {
                "name": info["name"],
                "completed_courses": sorted(info["completed_courses"]),
            }
        self.storage.save_students(raw)

    def reload(self):
        self.dict = StudentDictionary()
        self._load()

    def add_student(self, student_id, name):
        student_id = student_id.strip()
        name = name.strip()
        if not validate_student_id(student_id):
            return False, "Invalid student ID."
        if not validate_name(name):
            return False, "Invalid student name."
        if self.dict.student_exist(student_id):
            return False, "Student ID already exists."
        self.dict.add_student(student_id, name)
        self._save()
        return True, "Student registered successfully."

    def delete_student(self, student_id):
        if not self.dict.student_exist(student_id):
            return False, "Student not found."

        # Remove active course memberships and matching records before deleting
        # the student, so rosters and enrollment history do not retain a ghost.
        from services.course_service import CourseService
        from services.enrollment_service import EnrollmentService

        course_service = CourseService(self.storage)
        enrollment_service = EnrollmentService(
            self.storage, student_service=self, course_service=course_service)
        enrolled_courses = enrollment_service.enroll_set.get_courses_of_student(
            student_id)
        for course_code in enrolled_courses:
            enrollment_service.drop(student_id, course_code)

        self.dict.delete_student(student_id)
        self._save()
        return True, "Student deleted."

    def get_all_students(self):
        return self.dict.get_all_student()

    def get_student(self, student_id):
        return self.dict.get_student(student_id)

    # ---- self-implemented searching -----------------------------
    def search_by_id(self, student_id):
        return linear_search_by_id(self.dict.get_all_student(), student_id.strip())

    def search_by_name(self, name):
        records = [
            {"student_id": sid, "name": info["name"]}
            for sid, info in self.dict.get_all_student().items()
        ]
        record = linear_search_by_name(records, name)
        if record is None:
            return []
        sid = record["student_id"]
        return [(sid, self.dict.get_student(sid))]

    def mark_completed(self, student_id, course_code):
        if self.dict.get_student(student_id) is None:
            return False, "Student not found."
        self.dict.add_completed_course(student_id, course_code.upper().strip())
        self._save()
        return True, "Course marked as completed."

    def has_completed(self, student_id, course_code):
        return self.dict.has_completed(student_id, course_code)

    # ---- self-implemented sorting ------------------------------
    def sorted_students(self):
        records = [
            {"student_id": sid, "name": info["name"]}
            for sid, info in self.dict.get_all_student().items()
        ]
        ordered = bubble_sort_by_name(records)
        return [(r["student_id"], self.dict.get_student(r["student_id"]))
                for r in ordered]
