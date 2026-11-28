from data_structures.course_dictionary import CourseDictionary


# ---------- SAMPLE DATASET ----------
def make_sample_dictionary():
    courses = CourseDictionary()
    courses.add_course("CS101", "Intro to Programming", 2)
    courses.add_course("CS102", "Data Structures", 1, ["CS101"])
    courses.add_course("CS201", "Algorithms", 3, ["CS101", "CS102"])
    return courses


# ---------- __init__ ----------
def test_new_dictionary_is_empty():
    courses = CourseDictionary()
    assert courses.courses == {}


# ---------- add_course() ----------
def test_add_course_normal():
    courses = CourseDictionary()
    assert courses.add_course("CS101", "Intro", 30) is True
    assert "CS101" in courses.courses


def test_add_course_saves_correct_details():
    courses = CourseDictionary()
    courses.add_course("CS102", "Data Structures", 25, ["CS101"])
    course = courses.courses["CS102"]
    assert course["name"] == "Data Structures"
    assert course["capacity"] == 25
    assert course["enrolled"] == set()
    assert course["prerequisites"] == {"CS101"}


def test_add_course_without_prerequisites_is_empty_set():
    courses = CourseDictionary()
    courses.add_course("CS101", "Intro", 30)
    assert courses.courses["CS101"]["prerequisites"] == set()


def test_add_course_duplicate_returns_false():
    courses = CourseDictionary()
    courses.add_course("CS101", "Intro", 30)
    assert courses.add_course("CS101", "Another Name", 10) is False


def test_add_course_duplicate_keeps_original():
    courses = CourseDictionary()
    courses.add_course("CS101", "Intro", 30)
    courses.add_course("CS101", "Another Name", 10)
    assert courses.courses["CS101"]["name"] == "Intro"
    assert courses.courses["CS101"]["capacity"] == 30


# ---------- get_course() ----------
def test_get_course_found():
    courses = make_sample_dictionary()
    course = courses.get_course("CS101")
    assert course["name"] == "Intro to Programming"
    assert course["capacity"] == 2


def test_get_course_not_found_returns_none():
    courses = make_sample_dictionary()
    assert courses.get_course("XXX999") is None


def test_get_course_empty_dictionary():
    courses = CourseDictionary()
    assert courses.get_course("CS101") is None


# ---------- course_exists() ----------
def test_course_exists_true():
    courses = make_sample_dictionary()
    assert courses.course_exists("CS101") is True


def test_course_exists_false():
    courses = make_sample_dictionary()
    assert courses.course_exists("XXX999") is False


def test_course_exists_empty_dictionary():
    courses = CourseDictionary()
    assert courses.course_exists("CS101") is False


# ---------- has_slot() ----------
def test_has_slot_true_when_empty():
    courses = make_sample_dictionary()
    assert courses.has_slot("CS101") is True


def test_has_slot_true_when_partly_filled():
    courses = make_sample_dictionary()
    courses.enroll_student("CS101", "2024-001")  # capacity is 2
    assert courses.has_slot("CS101") is True


def test_has_slot_false_when_full():
    courses = make_sample_dictionary()
    courses.enroll_student("CS102", "2024-001")  # capacity is 1
    assert courses.has_slot("CS102") is False


def test_has_slot_false_when_capacity_is_zero():
    courses = CourseDictionary()
    courses.add_course("CS999", "Closed Course", 0)
    assert courses.has_slot("CS999") is False


def test_has_slot_course_not_found():
    courses = make_sample_dictionary()
    assert courses.has_slot("XXX999") is False


# ---------- enroll_student() ----------
def test_enroll_student_normal():
    courses = make_sample_dictionary()
    assert courses.enroll_student("CS101", "2024-001") is True
    assert "2024-001" in courses.courses["CS101"]["enrolled"]


def test_enroll_student_multiple_students():
    courses = make_sample_dictionary()
    courses.enroll_student("CS101", "2024-001")
    courses.enroll_student("CS101", "2024-002")
    assert courses.courses["CS101"]["enrolled"] == {"2024-001", "2024-002"}


def test_enroll_student_course_full_returns_false():
    courses = make_sample_dictionary()
    courses.enroll_student("CS102", "2024-001")  # capacity is 1
    assert courses.enroll_student("CS102", "2024-002") is False
    assert courses.courses["CS102"]["enrolled"] == {"2024-001"}


def test_enroll_student_course_not_found():
    courses = make_sample_dictionary()
    assert courses.enroll_student("XXX999", "2024-001") is False


def test_enroll_student_same_student_twice_is_stored_once():
    courses = make_sample_dictionary()
    courses.enroll_student("CS101", "2024-001")
    courses.enroll_student("CS101", "2024-001")
    assert len(courses.courses["CS101"]["enrolled"]) == 1


# ---------- drop_student() ----------
def test_drop_student_normal():
    courses = make_sample_dictionary()
    courses.enroll_student("CS101", "2024-001")
    assert courses.drop_student("CS101", "2024-001") is True
    assert "2024-001" not in courses.courses["CS101"]["enrolled"]


def test_drop_student_frees_slot():
    courses = make_sample_dictionary()
    courses.enroll_student("CS102", "2024-001")  # now full
    courses.drop_student("CS102", "2024-001")
    assert courses.has_slot("CS102") is True
    assert courses.enroll_student("CS102", "2024-002") is True


def test_drop_student_not_enrolled_does_not_crash():
    courses = make_sample_dictionary()
    # student was never enrolled; the code uses discard(), so this is safe
    assert courses.drop_student("CS101", "9999-999") is True
    assert courses.courses["CS101"]["enrolled"] == set()


def test_drop_student_course_not_found():
    courses = make_sample_dictionary()
    assert courses.drop_student("XXX999", "2024-001") is False


# ---------- meets_prerequisites() ----------
def test_meets_prerequisites_no_prerequisites():
    courses = make_sample_dictionary()
    assert courses.meets_prerequisites("CS101", []) is True


def test_meets_prerequisites_all_completed():
    courses = make_sample_dictionary()
    assert courses.meets_prerequisites("CS201", ["CS101", "CS102"]) is True


def test_meets_prerequisites_extra_completed_courses_ok():
    courses = make_sample_dictionary()
    assert courses.meets_prerequisites("CS102", ["CS101", "MA101"]) is True


def test_meets_prerequisites_missing_one():
    courses = make_sample_dictionary()
    assert courses.meets_prerequisites("CS201", ["CS101"]) is False


def test_meets_prerequisites_none_completed():
    courses = make_sample_dictionary()
    assert courses.meets_prerequisites("CS102", []) is False


def test_meets_prerequisites_works_with_set():
    courses = make_sample_dictionary()
    assert courses.meets_prerequisites("CS102", {"CS101"}) is True


def test_meets_prerequisites_course_not_found():
    courses = make_sample_dictionary()
    assert courses.meets_prerequisites("XXX999", ["CS101"]) is False


# ---------- get_all_courses() ----------
def test_get_all_courses_normal():
    courses = make_sample_dictionary()
    all_courses = courses.get_all_courses()
    assert set(all_courses.keys()) == {"CS101", "CS102", "CS201"}


def test_get_all_courses_empty():
    courses = CourseDictionary()
    assert courses.get_all_courses() == {}
