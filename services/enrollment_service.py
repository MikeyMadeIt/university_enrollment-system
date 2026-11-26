"""Enrollment rules using the original enrollment structures and graph modules."""

from datetime import datetime

from algorithms.bfs import bfs, bfs_levels
from algorithms.dfs import dfs
from algorithms.prerequisite_graph import build_prerequisite_graph
from algorithms.topological_sort import topological_sort
from data_structures.enrollment_list import EnrollmentList
from data_structures.enrollment_set import EnrollmentSet


class EnrollmentService:
    def __init__(self, storage, student_service, course_service):
        self.storage = storage
        self.student_service = student_service
        self.course_service = course_service
        self.enrollments = EnrollmentSet()
        self.records = EnrollmentList()
        for row in storage.load("enrollments.json", []):
            if not isinstance(row, dict):
                continue
            sid = str(row.get("student_id", "")).strip().upper()
            code = str(row.get("course_code", "")).strip().upper()
            if not sid or not code or not self.enrollments.add_enrollment(sid, code):
                continue
            self.records.add_record(sid, code, row.get("timestamp"))
            if self.course_service.courses.course_exists(code):
                self.course_service.courses.enroll_student(code, sid)

    def enroll(self, student_id, course_code):
        sid, code = (student_id or "").strip().upper(), (course_code or "").strip().upper()
        student, course = self.student_service.get(sid), self.course_service.get(code)
        if student is None:
            raise ValueError(f"Student {sid} not found")
        if course is None:
            raise ValueError(f"Course {code} not found")
        if self.enrollments.is_duplicate(sid, code):
            raise ValueError("Student is already enrolled in this course")
        completed = {value.upper() for value in student.get("completed_courses", [])}
        if code in completed:
            raise ValueError("Student has already completed this course")

        # The designated graph uses prerequisite -> dependent edges. Walk that
        # graph with the designated DFS to find every prerequisite of this course.
        graph = self.course_service.prerequisite_graph()
        required = {node for node in graph if node != code and code in dfs(graph, node)}
        missing = required - completed
        if not self.course_service.courses.meets_prerequisites(code, completed) or missing:
            raise ValueError(f"Prerequisites not met. Missing: {', '.join(sorted(missing))}")
        if len(self.enrollments.get_students_of_course(code)) >= course["capacity"]:
            raise ValueError("Course is full")
        if not self.course_service.courses.has_slot(code):
            raise ValueError("Course is full")
        if not self.enrollments.add_enrollment(sid, code):
            raise ValueError("Student is already enrolled in this course")
        if not self.course_service.courses.enroll_student(code, sid):
            self.enrollments.remove_enrollment(sid, code)
            raise ValueError("Course is full")
        record = self.records.add_record(sid, code,
                                         datetime.now().astimezone().isoformat(timespec="seconds"))
        self._persist()
        return record

    def drop(self, student_id, course_code):
        sid, code = (student_id or "").strip().upper(), (course_code or "").strip().upper()
        if not self.enrollments.remove_enrollment(sid, code):
            raise ValueError("Enrollment not found")
        self.course_service.courses.drop_student(code, sid)
        self.records.records[:] = [r for r in self.records.get_all_records()
                                   if (r["student_id"], r["course_code"]) != (sid, code)]
        self._persist()

    def drop_all_for_student(self, student_id):
        sid = (student_id or "").strip().upper()
        codes = list(self.enrollments.get_courses_of_student(sid))
        for code in codes:
            self.enrollments.remove_enrollment(sid, code)
            self.course_service.courses.drop_student(code, sid)
        self.records.records[:] = [r for r in self.records.get_all_records() if r["student_id"] != sid]
        if codes:
            self._persist()

    def drop_all_for_course(self, course_code):
        code = (course_code or "").strip().upper()
        students = list(self.enrollments.get_students_of_course(code))
        for sid in students:
            self.enrollments.remove_enrollment(sid, code)
            self.course_service.courses.drop_student(code, sid)
        self.records.records[:] = [r for r in self.records.get_all_records() if r["course_code"] != code]
        if students:
            self._persist()

    def count_for_course(self, course_code):
        return len(self.enrollments.get_students_of_course((course_code or "").strip().upper()))

    def for_student(self, student_id):
        return self.records.filter_by_student((student_id or "").strip().upper())

    def for_course(self, course_code):
        return self.records.filter_by_course((course_code or "").strip().upper())

    def all(self):
        return self.records.get_all_records()

    def prerequisite_dfs(self, course_code):
        return dfs(self.course_service.prerequisite_graph(), course_code.strip().upper())

    def prerequisite_bfs(self, course_code):
        return bfs(self.course_service.prerequisite_graph(), course_code.strip().upper())

    def prerequisite_levels(self, course_code):
        return bfs_levels(self.course_service.prerequisite_graph(), course_code.strip().upper())

    def prerequisite_order(self):
        return topological_sort(self.course_service.prerequisite_graph())

    def _persist(self):
        self.storage.save("enrollments.json", self.all())
