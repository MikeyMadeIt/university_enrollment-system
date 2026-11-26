"""Enrollment rules: capacity, duplicates, prerequisites, completion."""

from algorithms.graph import build_prereq_graph, prerequisites_met


class EnrollmentService:
    def __init__(self, storage, collection, student_service, course_service):
        self.storage = storage
        self.collection = collection
        self.student_service = student_service
        self.course_service = course_service

    def enroll(self, student_id, course_code):
        student = self.student_service.get(student_id)
        if student is None:
            raise ValueError(f"Student {student_id} not found")

        course = self.course_service.get(course_code)
        if course is None:
            raise ValueError(f"Course {course_code} not found")

        if self.collection.exists(student_id, course_code):
            raise ValueError("Student is already enrolled in this course")

        completed = set(c.upper() for c in student.get("completed_courses", []))
        if course_code in completed:
            raise ValueError("Student has already completed this course")

        if self.collection.count_for_course(course_code) >= course["capacity"]:
            raise ValueError("Course is full")

        graph = build_prereq_graph(self.course_service.all())
        if not prerequisites_met(course_code, completed, graph):
            missing = sorted(
                set(c for c in self._required_prereqs(course_code, graph))
                - completed
            )
            raise ValueError(f"Prerequisites not met. Missing: {', '.join(missing)}")

        self.collection.add({"student_id": student_id, "course_code": course_code})
        self._persist()

    def drop(self, student_id, course_code):
        if not self.collection.remove(student_id, course_code):
            raise ValueError("Enrollment not found")
        self._persist()

    def drop_all_for_student(self, student_id):
        changed = False
        for e in self.collection.for_student(student_id):
            self.collection.remove(student_id, e["course_code"])
            changed = True
        if changed:
            self._persist()

    def drop_all_for_course(self, course_code):
        changed = False
        for e in self.collection.for_course(course_code):
            self.collection.remove(e["student_id"], course_code)
            changed = True
        if changed:
            self._persist()

    def count_for_course(self, course_code):
        return self.collection.count_for_course(course_code)

    def all(self):
        return self.collection.all()

    @staticmethod
    def _required_prereqs(course_code, graph):
        from algorithms.graph import all_prerequisites
        return all_prerequisites(course_code, graph)

    def _persist(self):
        self.storage.save("enrollments.json", self.collection.all())