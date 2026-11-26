"""Enrollment reports ordered with the designated sorting implementation."""

from algorithms.sorting import bubble_sort_by_name


class ReportService:
    def __init__(self, student_service, course_service, enrollment_service):
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service

    def enrollment_report(self, sort_by="student_name"):
        students = {s["student_id"]: s for s in self.student_service.all()}
        courses = {c["course_code"]: c for c in self.course_service.all()}
        rows = []
        for enrollment in self.enrollment_service.all():
            student = students.get(enrollment["student_id"], {})
            course = courses.get(enrollment["course_code"], {})
            rows.append({**enrollment,
                         "student_name": student.get("name", "Unknown student"),
                         "course_name": course.get("title", "Unknown course")})
        allowed = {"student_name", "course_name", "student_id", "course_code"}
        sort_by = sort_by if sort_by in allowed else "student_name"
        sortable_rows = [{"name": row[sort_by], "row": row} for row in rows]
        return [entry["row"] for entry in bubble_sort_by_name(sortable_rows)]
