import tempfile

import pytest

from data_structures.enrollment_list import EnrollmentList
from data_structures.enrollment_set import EnrollmentSet
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from storage.json_storage import JsonStorage


def test_enrollment_set_and_list_operations():
    unique = EnrollmentSet()
    assert unique.add_enrollment("S1", "CS101")
    assert not unique.add_enrollment("S1", "CS101")
    assert unique.is_duplicate("S1", "CS101")
    assert unique.get_courses_of_student("S1") == {"CS101"}
    assert unique.get_students_of_course("CS101") == {"S1"}
    assert unique.remove_enrollment("S1", "CS101")

    records = EnrollmentList()
    records.add_record("S1", "CS101", "now")
    records.add_record("S2", "CS101", "later")
    assert len(records.filter_by_course("CS101")) == 2
    assert records.filter_by_student("S1")[0]["course_code"] == "CS101"


def test_enrollment_service_prerequisite_duplicate_capacity_and_persistence():
    with tempfile.TemporaryDirectory() as directory:
        storage = JsonStorage(directory)
        students, courses = StudentService(storage), CourseService(storage)
        enrollments = EnrollmentService(storage, students, courses)
        courses.add("CS101", "Intro", 2)
        courses.add("CS102", "Data Structures", 1, ["CS101"])
        courses.add("MA101", "Math", 1)
        students.add("S1", "Alice", completed=["CS101"])
        students.add("S2", "Bob")

        enrollments.enroll("S1", "CS102")
        assert enrollments.count_for_course("CS102") == 1
        with pytest.raises(ValueError, match="already enrolled"):
            enrollments.enroll("S1", "CS102")
        with pytest.raises(ValueError, match="Prerequisites"):
            enrollments.enroll("S2", "CS102")
        enrollments.enroll("S2", "MA101")
        with pytest.raises(ValueError, match="full"):
            enrollments.enroll("S1", "MA101")
        assert enrollments.count_for_course("MA101") == 1
        assert not enrollments.enrollments.is_duplicate("S1", "MA101")

        reopened = EnrollmentService(storage, StudentService(storage), CourseService(storage))
        assert reopened.count_for_course("CS102") == 1
        assert reopened.for_course("CS102")[0]["student_id"] == "S1"


def test_enrollment_service_graph_helpers_errors_and_drop_persistence(tmp_path):
    storage = JsonStorage(str(tmp_path))
    students, courses = StudentService(storage), CourseService(storage)
    enrollments = EnrollmentService(storage, students, courses)

    courses.add("CS101", "Intro", 3)
    courses.add("CS102", "Data Structures", 3, ["CS101"])
    courses.add("CS201", "Algorithms", 3, ["CS102"])
    students.add("S1", "Alice", completed=["CS101", "CS102"])

    assert enrollments.prerequisite_dfs("CS101") == ["CS101", "CS102", "CS201"]
    assert enrollments.prerequisite_bfs("CS101") == ["CS101", "CS102", "CS201"]
    assert enrollments.prerequisite_levels("CS101") == {
        "CS101": 0, "CS102": 1, "CS201": 2
    }
    assert enrollments.prerequisite_order() == ["CS101", "CS102", "CS201"]

    with pytest.raises(ValueError, match="Student MISSING not found"):
        enrollments.enroll("MISSING", "CS201")
    with pytest.raises(ValueError, match="Course MISSING not found"):
        enrollments.enroll("S1", "MISSING")

    record = enrollments.enroll("S1", "CS201")
    assert record["student_id"] == "S1"
    enrollments.drop("S1", "CS201")
    assert enrollments.all() == []
    assert EnrollmentService(storage, StudentService(storage), CourseService(storage)).all() == []

    with pytest.raises(ValueError, match="Enrollment not found"):
        enrollments.drop("S1", "CS201")


def test_completed_course_cannot_be_taken_again(tmp_path):
    storage = JsonStorage(str(tmp_path))
    students, courses = StudentService(storage), CourseService(storage)
    enrollments = EnrollmentService(storage, students, courses)
    courses.add("CS101", "Intro", 2)
    students.add("S1", "Alice", completed=["CS101"])

    with pytest.raises(ValueError, match="already completed"):
        enrollments.enroll("S1", "CS101")


def test_drop_all_operations_keep_services_and_json_in_sync(tmp_path):
    storage = JsonStorage(str(tmp_path))
    students, courses = StudentService(storage), CourseService(storage)
    enrollments = EnrollmentService(storage, students, courses)
    courses.add("CS101", "Intro", 3)
    courses.add("MA101", "Math", 3)
    students.add("S1", "Alice")
    students.add("S2", "Bob")
    enrollments.enroll("S1", "CS101")
    enrollments.enroll("S2", "CS101")
    enrollments.enroll("S1", "MA101")

    enrollments.drop_all_for_student("S1")
    assert enrollments.count_for_course("CS101") == 1
    assert enrollments.count_for_course("MA101") == 0
    assert [row["student_id"] for row in enrollments.all()] == ["S2"]

    enrollments.drop_all_for_course("CS101")
    assert enrollments.all() == []
    assert EnrollmentService(storage, StudentService(storage), CourseService(storage)).all() == []


def test_enrollment_service_skips_malformed_rows_and_normalizes_identifiers(tmp_path):
    storage = JsonStorage(str(tmp_path))
    storage.save("courses.json", [{
        "course_code": "CS101", "title": "Intro", "capacity": 2,
        "prerequisites": [],
    }])
    storage.save("enrollments.json", [
        None,
        {"student_id": " s1 ", "course_code": " cs101 ", "timestamp": "now"},
        {"student_id": "", "course_code": "CS101"},
    ])
    students, courses = StudentService(storage), CourseService(storage)

    enrollments = EnrollmentService(storage, students, courses)
    assert enrollments.all() == [{
        "student_id": "S1", "course_code": "CS101", "timestamp": "now"
    }]
    assert enrollments.count_for_course("cs101") == 1
