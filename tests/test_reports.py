from services.report_service import ReportService


class StubService:
    def __init__(self, rows):
        self.rows = rows

    def all(self):
        return list(self.rows)


def test_enrollment_report_joins_records_and_sorts_by_requested_column():
    students = StubService([
        {"student_id": "S2", "name": "Zoe"},
        {"student_id": "S1", "name": "Amy"},
    ])
    courses = StubService([
        {"course_code": "CS102", "title": "Zoology"},
        {"course_code": "CS101", "title": "Algebra"},
    ])
    enrollments = StubService([
        {"student_id": "S2", "course_code": "CS102", "timestamp": "t2"},
        {"student_id": "S1", "course_code": "CS101", "timestamp": "t1"},
    ])
    reports = ReportService(students, courses, enrollments)

    by_course = reports.enrollment_report("course_name")
    assert [row["course_name"] for row in by_course] == ["Algebra", "Zoology"]
    assert by_course[0]["student_name"] == "Amy"
    assert by_course[1]["timestamp"] == "t2"

    default_order = reports.enrollment_report("unsupported-column")
    assert [row["student_name"] for row in default_order] == ["Amy", "Zoe"]


def test_enrollment_report_handles_missing_referenced_records():
    reports = ReportService(
        StubService([]),
        StubService([]),
        StubService([{"student_id": "S404", "course_code": "CS404"}]),
    )

    report = reports.enrollment_report()
    assert report == [{
        "student_id": "S404",
        "course_code": "CS404",
        "student_name": "Unknown student",
        "course_name": "Unknown course",
    }]
