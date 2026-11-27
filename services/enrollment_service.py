from datetime import datetime
from storage.json_storage import JsonStorage
from services.student_service import StudentService
from services.course_service import CourseService
from data_structures.enrollment_set import EnrollmentSet
from data_structures.enrollment_list import EnrollmentList


class EnrollmentService:
    def __init__(self, storage=None, student_service=None, course_service=None):
        self.storage = storage or JsonStorage()
        self.student_service = student_service or StudentService(self.storage)
        self.course_service = course_service or CourseService(self.storage)
        self.enroll_set = EnrollmentSet()
        self.list = EnrollmentList()
        self._load()

    def _load(self):
        # Rebuild EnrollmentSet from courses (source of truth)
        for code, info in self.course_service.get_all_courses().items():
            for sid in info.get("enrolled", []):
                self.enroll_set.add_enrollment(sid, code)
        # Rebuild transaction log
        for r in self.storage.load_enrollments():
            self.list.add_record(r["student_id"], r["course_code"],
                                 r.get("timestamp"))

    def _enrich(self, records):
        out = []
        for r in records:
            s = self.student_service.get_student(r["student_id"])
            c = self.course_service.get_course(r["course_code"])
            out.append({
                "student_id": r["student_id"],
                "student_name": s["name"] if s else "(unknown)",
                "course_code": r["course_code"],
                "course_name": c["name"] if c else "(unknown)",
                "timestamp": r.get("timestamp"),
            })
        return out

    def _save(self):
        self.storage.save_enrollments(
            self._enrich(self.list.get_all_records()))

    def reload(self):
        self.enroll_set = EnrollmentSet()
        self.list = EnrollmentList()
        self._load()

    def enroll(self, student_id, course_code):
        student_id = student_id.strip()
        course_code = course_code.strip().upper()

        student = self.student_service.get_student(student_id)
        if not student:
            return False, "Student not found."

        course = self.course_service.get_course(course_code)
        if not course:
            return False, "Course not found."

        if not self.course_service.has_slot(course_code):
            return False, "Course is already full."

        if self.enroll_set.is_duplicate(student_id, course_code):
            return False, "Student is already enrolled in this course."

        if not self.course_service.meets_prerequisites(
                course_code, student["completed_courses"]):
            missing = set(course["prerequisites"]) - set(student["completed_courses"])
            return False, f"Missing prerequisites: {', '.join(sorted(missing))}"

        ok = self.course_service.add_enrollment(course_code, student_id)
        if not ok:
            return False, "Failed to add enrollment."

        self.enroll_set.add_enrollment(student_id, course_code)
        self.list.add_record(student_id, course_code,
                             datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self._save()
        return True, "Enrollment successful."

    def drop(self, student_id, course_code):
        course_code = course_code.strip().upper()
        ok = self.course_service.remove_enrollment(course_code, student_id)
        if not ok:
            return False, "Enrollment not found."
        self.enroll_set.remove_enrollment(student_id, course_code)
        self.list.records = [
            r for r in self.list.records
            if not (r["student_id"] == student_id and
                    r["course_code"] == course_code)
        ]
        self._save()
        return True, "Enrollment dropped."

    def get_all_records(self):
        return self._enrich(self.list.get_all_records())

    def get_by_student(self, student_id):
        return self._enrich(self.list.filter_by_student(student_id))

    def get_by_course(self, course_code):
        return self._enrich(self.list.filter_by_course(course_code.upper()))
