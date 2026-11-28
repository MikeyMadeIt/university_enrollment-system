from data_structures.enrollment_list import EnrollmentList


# ---------- SAMPLE DATASET ----------
def make_sample_list():
    log = EnrollmentList()
    log.add_record("2024-001", "CS101", "2026-11-01")
    log.add_record("2024-001", "CS102", "2026-11-02")
    log.add_record("2024-002", "CS101", "2026-11-03")
    return log


# ---------- __init__ ----------
def test_new_list_is_empty():
    log = EnrollmentList()
    assert log.records == []


# ---------- add_record() ----------
def test_add_record_returns_record():
    log = EnrollmentList()
    record = log.add_record("2024-001", "CS101", "2026-11-01")
    assert record == {
        "student_id": "2024-001",
        "course_code": "CS101",
        "timestamp": "2026-11-01",
    }


def test_add_record_saves_to_list():
    log = EnrollmentList()
    log.add_record("2024-001", "CS101")
    assert len(log.records) == 1


def test_add_record_without_timestamp_is_none():
    log = EnrollmentList()
    record = log.add_record("2024-001", "CS101")
    assert record["timestamp"] is None


def test_add_record_keeps_order():
    log = EnrollmentList()
    log.add_record("2024-001", "CS101")
    log.add_record("2024-002", "CS102")
    assert log.records[0]["student_id"] == "2024-001"
    assert log.records[1]["student_id"] == "2024-002"


# ---------- get_all_records() ----------
def test_get_all_records_normal():
    log = make_sample_list()
    assert len(log.get_all_records()) == 3


def test_get_all_records_empty():
    log = EnrollmentList()
    assert log.get_all_records() == []


# ---------- filter_by_student() ----------
def test_filter_by_student_normal():
    log = make_sample_list()
    result = log.filter_by_student("2024-001")
    assert len(result) == 2
    assert all(r["student_id"] == "2024-001" for r in result)


def test_filter_by_student_not_found():
    log = make_sample_list()
    assert log.filter_by_student("9999-999") == []


def test_filter_by_student_empty_list():
    log = EnrollmentList()
    assert log.filter_by_student("2024-001") == []


# ---------- filter_by_course() ----------
def test_filter_by_course_normal():
    log = make_sample_list()
    result = log.filter_by_course("CS101")
    assert len(result) == 2
    assert all(r["course_code"] == "CS101" for r in result)


def test_filter_by_course_not_found():
    log = make_sample_list()
    assert log.filter_by_course("XXX999") == []


def test_filter_by_course_empty_list():
    log = EnrollmentList()
    assert log.filter_by_course("CS101") == []
