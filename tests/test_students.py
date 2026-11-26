import tempfile

import pytest

from data_structures.student_dictionary import StudentDictionary
from services.student_service import StudentService
from storage.json_storage import JsonStorage


def test_student_dictionary_and_service_search_persistence():
    dictionary = StudentDictionary()
    assert dictionary.add_student("S1", "Alice")
    assert not dictionary.add_student("S1", "Duplicate")
    assert dictionary.student_exist("S1")
    assert dictionary.add_completed_course("S1", "CS101")
    assert dictionary.has_completed("S1", "CS101")
    assert dictionary.delete_student("S1")

    with tempfile.TemporaryDirectory() as directory:
        storage = JsonStorage(directory)
        students = StudentService(storage)
        students.add("S1", "Alice", "alice@example.test", ["CS101"])
        assert students.search("s1")["name"] == "Alice"
        assert students.search("alice")["student_id"] == "S1"
        assert students.search("") is None
        assert students.search("missing") is None
        assert StudentService(storage).get("S1")["completed_courses"] == ["CS101"]


def test_student_service_validates_duplicates_and_persists_removal(tmp_path):
    storage = JsonStorage(str(tmp_path))
    students = StudentService(storage)

    with pytest.raises(ValueError, match="required"):
        students.add("", "Alice")
    with pytest.raises(ValueError, match="required"):
        students.add("S1", " ")

    students.add("s1", "Alice")
    with pytest.raises(ValueError, match="already exists"):
        students.add("S1", "Another Alice")
    with pytest.raises(ValueError, match="not found"):
        students.add_completed_course("UNKNOWN", "CS101")
    with pytest.raises(ValueError, match="required"):
        students.add_completed_course("S1", " ")

    students.remove("s1")
    assert students.all() == []
    assert StudentService(storage).all() == []

    with pytest.raises(ValueError, match="not found"):
        students.remove("S1")


def test_student_service_skips_malformed_rows_without_losing_valid_data(tmp_path):
    storage = JsonStorage(str(tmp_path))
    storage.save("students.json", [
        None,
        {"id": " s1 ", "name": " Alice ", "completed_courses": "CS101"},
        {"student_id": "S2", "name": 17},
    ])

    students = StudentService(storage)
    assert students.all() == [{
        "student_id": "S1",
        "name": "Alice",
        "email": "",
        "completed_courses": [],
    }]
