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

        reopened = EnrollmentService(storage, StudentService(storage), CourseService(storage))
        assert reopened.count_for_course("CS102") == 1
        assert reopened.for_course("CS102")[0]["student_id"] == "S1"
