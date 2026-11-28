from data_structures.student_dictionary import StudentDictionary


# ---------- SAMPLE DATASET ----------
def make_sample_dictionary():
    students = StudentDictionary()
    students.add_student("2024-001", "Juan Dela Cruz")
    students.add_student("2024-002", "Maria Santos")
    students.add_student("2024-003", "Pedro Reyes")
    return students


# ---------- __init__ ----------
def test_new_dictionary_is_empty():
    students = StudentDictionary()
    assert students.students == {}


# ---------- add_student() ----------
def test_add_student_normal():
    students = StudentDictionary()
    assert students.add_student("2024-001", "Juan Dela Cruz") is True
    assert "2024-001" in students.students


def test_add_student_saves_correct_details():
    students = StudentDictionary()
    students.add_student("2024-001", "Juan Dela Cruz")
    student = students.students["2024-001"]
    assert student["name"] == "Juan Dela Cruz"
    assert student["completed_courses"] == set()


def test_add_student_duplicate_returns_false():
    students = StudentDictionary()
    students.add_student("2024-001", "Juan Dela Cruz")
    assert students.add_student("2024-001", "Someone Else") is False


def test_add_student_duplicate_keeps_original():
    students = StudentDictionary()
    students.add_student("2024-001", "Juan Dela Cruz")
    students.add_student("2024-001", "Someone Else")
    assert students.students["2024-001"]["name"] == "Juan Dela Cruz"


def test_add_student_multiple_students():
    students = make_sample_dictionary()
    assert len(students.students) == 3


# ---------- get_student() ----------
def test_get_student_found():
    students = make_sample_dictionary()
    student = students.get_student("2024-002")
    assert student["name"] == "Maria Santos"


def test_get_student_not_found_returns_none():
    students = make_sample_dictionary()
    assert students.get_student("9999-999") is None


def test_get_student_empty_dictionary():
    students = StudentDictionary()
    assert students.get_student("2024-001") is None


# ---------- student_exist() ----------
def test_student_exist_true():
    students = make_sample_dictionary()
    assert students.student_exist("2024-001") is True


def test_student_exist_false():
    students = make_sample_dictionary()
    assert students.student_exist("9999-999") is False


def test_student_exist_empty_dictionary():
    students = StudentDictionary()
    assert students.student_exist("2024-001") is False


# ---------- add_completed_course() ----------
def test_add_completed_course_normal():
    students = make_sample_dictionary()
    assert students.add_completed_course("2024-001", "CS101") is True
    assert "CS101" in students.students["2024-001"]["completed_courses"]


def test_add_completed_course_multiple_courses():
    students = make_sample_dictionary()
    students.add_completed_course("2024-001", "CS101")
    students.add_completed_course("2024-001", "CS102")
    assert students.students["2024-001"]["completed_courses"] == {"CS101", "CS102"}


def test_add_completed_course_same_course_twice_stored_once():
    students = make_sample_dictionary()
    students.add_completed_course("2024-001", "CS101")
    students.add_completed_course("2024-001", "CS101")
    assert len(students.students["2024-001"]["completed_courses"]) == 1


def test_add_completed_course_only_affects_that_student():
    students = make_sample_dictionary()
    students.add_completed_course("2024-001", "CS101")
    assert students.students["2024-002"]["completed_courses"] == set()


def test_add_completed_course_student_not_found():
    students = make_sample_dictionary()
    assert students.add_completed_course("9999-999", "CS101") is False


# ---------- has_completed() ----------
def test_has_completed_true():
    students = make_sample_dictionary()
    students.add_completed_course("2024-001", "CS101")
    assert students.has_completed("2024-001", "CS101") is True


def test_has_completed_false_not_taken():
    students = make_sample_dictionary()
    assert students.has_completed("2024-001", "CS101") is False


def test_has_completed_false_different_course():
    students = make_sample_dictionary()
    students.add_completed_course("2024-001", "CS101")
    assert students.has_completed("2024-001", "CS102") is False


def test_has_completed_student_not_found():
    students = make_sample_dictionary()
    assert students.has_completed("9999-999", "CS101") is False


# ---------- delete_student() ----------
def test_delete_student_normal():
    students = make_sample_dictionary()
    assert students.delete_student("2024-001") is True
    assert students.student_exist("2024-001") is False


def test_delete_student_keeps_others():
    students = make_sample_dictionary()
    students.delete_student("2024-001")
    assert len(students.students) == 2
    assert students.student_exist("2024-002") is True


def test_delete_student_not_found():
    students = make_sample_dictionary()
    assert students.delete_student("9999-999") is False
    assert len(students.students) == 3


def test_delete_student_twice_second_returns_false():
    students = make_sample_dictionary()
    students.delete_student("2024-001")
    assert students.delete_student("2024-001") is False


def test_delete_student_then_add_again():
    students = make_sample_dictionary()
    students.delete_student("2024-001")
    assert students.add_student("2024-001", "New Juan") is True


# ---------- get_all_student() ----------
def test_get_all_student_normal():
    students = make_sample_dictionary()
    all_students = students.get_all_student()
    assert set(all_students.keys()) == {"2024-001", "2024-002", "2024-003"}


def test_get_all_student_empty():
    students = StudentDictionary()
    assert students.get_all_student() == {}
