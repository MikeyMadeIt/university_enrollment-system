from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from storage.json_storage import JsonStorage


def make_services(tmp_path):
    storage = JsonStorage(tmp_path)
    students = StudentService(storage)
    courses = CourseService(storage)
    enrollments = EnrollmentService(storage, students, courses)
    return students, courses, enrollments


def test_enrollment_drop_removes_membership_and_record(tmp_path):
    students, courses, enrollments = make_services(tmp_path)
    assert students.add_student("2026-100", "Test Student")[0]
    assert courses.add_course("CS101", "Intro to Computing", 2)[0]

    assert enrollments.enroll("2026-100", "CS101")[0]
    assert len(enrollments.get_all_records()) == 1
    assert enrollments.drop("2026-100", "CS101")[0]
    assert courses.get_roster("CS101") == []
    assert enrollments.get_all_records() == []

    # A dropped course can be selected and enrolled in again.
    assert enrollments.enroll("2026-100", "CS101")[0]


def test_deleting_student_cleans_up_active_enrollments_and_records(tmp_path):
    students, courses, enrollments = make_services(tmp_path)
    assert students.add_student("2026-101", "Another Student")[0]
    assert courses.add_course("IT101", "Intro to IT", 2)[0]
    assert enrollments.enroll("2026-101", "IT101")[0]

    assert students.delete_student("2026-101")[0]
    assert students.get_student("2026-101") is None
    courses.reload()
    enrollments.reload()
    assert courses.get_roster("IT101") == []
    assert enrollments.get_all_records() == []


def test_course_deletion_protects_enrolled_and_prerequisite_courses(tmp_path):
    _, courses, enrollments = make_services(tmp_path)
    assert courses.add_course("CS101", "Intro to Computing", 2)[0]
    assert courses.add_course("CS102", "Data Structures", 2, ["CS101"])[0]

    ok, message = courses.delete_course("CS101")
    assert not ok
    assert "CS102" in message

    assert courses.add_course("IT101", "Intro to IT", 2)[0]
    # Create a student and enrollment through a fresh service pair.
    students = StudentService(courses.storage)
    assert students.add_student("2026-102", "Enrolled Student")[0]
    enrollment_service = EnrollmentService(
        courses.storage, students, courses)
    assert enrollment_service.enroll("2026-102", "IT101")[0]

    ok, message = courses.delete_course("IT101")
    assert not ok
    assert "enrolled students" in message
    assert enrollment_service.drop("2026-102", "IT101")[0]
    assert courses.delete_course("IT101")[0]


def test_json_storage_returns_expected_root_type(tmp_path):
    storage = JsonStorage(tmp_path)
    storage.save("students.json", ["wrong root"])

    assert storage.load_students() == {}
