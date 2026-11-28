from data_structures.enrollment_set import EnrollmentSet


# ---------- SAMPLE DATASET ----------
def make_sample_set():
    enrolled = EnrollmentSet()
    enrolled.add_enrollment("2024-001", "CS101")
    enrolled.add_enrollment("2024-001", "CS102")
    enrolled.add_enrollment("2024-002", "CS101")
    return enrolled


# ---------- __init__ ----------
def test_new_set_is_empty():
    enrolled = EnrollmentSet()
    assert enrolled.enrollments == set()


# ---------- add_enrollment() ----------
def test_add_enrollment_normal():
    enrolled = EnrollmentSet()
    assert enrolled.add_enrollment("2024-001", "CS101") is True
    assert ("2024-001", "CS101") in enrolled.enrollments


def test_add_enrollment_duplicate_returns_false():
    enrolled = EnrollmentSet()
    enrolled.add_enrollment("2024-001", "CS101")
    assert enrolled.add_enrollment("2024-001", "CS101") is False
    assert len(enrolled.enrollments) == 1


def test_add_enrollment_same_student_different_course():
    enrolled = EnrollmentSet()
    assert enrolled.add_enrollment("2024-001", "CS101") is True
    assert enrolled.add_enrollment("2024-001", "CS102") is True
    assert len(enrolled.enrollments) == 2


def test_add_enrollment_same_course_different_student():
    enrolled = EnrollmentSet()
    assert enrolled.add_enrollment("2024-001", "CS101") is True
    assert enrolled.add_enrollment("2024-002", "CS101") is True
    assert len(enrolled.enrollments) == 2


# ---------- is_duplicate() ----------
def test_is_duplicate_true():
    enrolled = make_sample_set()
    assert enrolled.is_duplicate("2024-001", "CS101") is True


def test_is_duplicate_false_not_enrolled():
    enrolled = make_sample_set()
    assert enrolled.is_duplicate("2024-002", "CS102") is False


def test_is_duplicate_empty_set():
    enrolled = EnrollmentSet()
    assert enrolled.is_duplicate("2024-001", "CS101") is False


# ---------- remove_enrollment() ----------
def test_remove_enrollment_normal():
    enrolled = make_sample_set()
    assert enrolled.remove_enrollment("2024-001", "CS101") is True
    assert enrolled.is_duplicate("2024-001", "CS101") is False


def test_remove_enrollment_not_found():
    enrolled = make_sample_set()
    assert enrolled.remove_enrollment("9999-999", "XXX999") is False
    assert len(enrolled.enrollments) == 3


def test_remove_enrollment_empty_set():
    enrolled = EnrollmentSet()
    assert enrolled.remove_enrollment("2024-001", "CS101") is False


def test_remove_then_add_again():
    enrolled = EnrollmentSet()
    enrolled.add_enrollment("2024-001", "CS101")
    enrolled.remove_enrollment("2024-001", "CS101")
    assert enrolled.add_enrollment("2024-001", "CS101") is True


# ---------- get_courses_of_student() ----------
def test_get_courses_of_student_normal():
    enrolled = make_sample_set()
    assert enrolled.get_courses_of_student("2024-001") == {"CS101", "CS102"}


def test_get_courses_of_student_one_course():
    enrolled = make_sample_set()
    assert enrolled.get_courses_of_student("2024-002") == {"CS101"}


def test_get_courses_of_student_not_found():
    enrolled = make_sample_set()
    assert enrolled.get_courses_of_student("9999-999") == set()


def test_get_courses_of_student_empty_set():
    enrolled = EnrollmentSet()
    assert enrolled.get_courses_of_student("2024-001") == set()


# ---------- get_students_of_course() ----------
def test_get_students_of_course_normal():
    enrolled = make_sample_set()
    assert enrolled.get_students_of_course("CS101") == {"2024-001", "2024-002"}


def test_get_students_of_course_one_student():
    enrolled = make_sample_set()
    assert enrolled.get_students_of_course("CS102") == {"2024-001"}


def test_get_students_of_course_not_found():
    enrolled = make_sample_set()
    assert enrolled.get_students_of_course("XXX999") == set()


def test_get_students_of_course_empty_set():
    enrolled = EnrollmentSet()
    assert enrolled.get_students_of_course("CS101") == set()
