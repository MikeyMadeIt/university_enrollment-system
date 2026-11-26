"""Launch the university enrollment desktop application."""

import os

from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.report_service import ReportService
from services.student_service import StudentService
from storage.json_storage import JsonStorage
from ui.app import run_app


def main():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    storage = JsonStorage(data_dir)
    students = StudentService(storage)
    courses = CourseService(storage)
    enrollments = EnrollmentService(storage, students, courses)
    reports = ReportService(students, courses, enrollments)
    run_app(students, courses, enrollments, reports)


if __name__ == "__main__":
    main()
