import tempfile

import pytest

from data_structures.course_dictionary import CourseDictionary
from services.course_service import CourseService
from storage.json_storage import JsonStorage


def test_course_dictionary_capacity_and_course_service_graph_search():
    dictionary = CourseDictionary()
    assert dictionary.add_course("CS101", "Intro", 1)
    assert dictionary.has_slot("CS101")
    assert dictionary.enroll_student("CS101", "S1")
    assert not dictionary.has_slot("CS101")

    with tempfile.TemporaryDirectory() as directory:
        courses = CourseService(JsonStorage(directory))
        courses.add("CS101", "Intro", 4)
        courses.add("CS102", "Data Structures", 2, ["CS101"])
        assert courses.search("data")[0]["course_code"] == "CS102"
        assert courses.prerequisite_graph() == {"CS101": ["CS102"], "CS102": []}
        assert CourseService(JsonStorage(directory)).get("CS102")["prerequisites"] == ["CS101"]


def test_course_service_validation_and_prerequisite_deletion_rules(tmp_path):
    storage = JsonStorage(str(tmp_path))
    courses = CourseService(storage)

    with pytest.raises(ValueError, match="required"):
        courses.add("", "Intro", 5)
    with pytest.raises(ValueError, match="integer"):
        courses.add("CS101", "Intro", "five")
    with pytest.raises(ValueError, match="positive"):
        courses.add("CS101", "Intro", 0)

    courses.add("CS101", "Intro", 5)
    with pytest.raises(ValueError, match="already exists"):
        courses.add("CS101", "Duplicate", 5)
    with pytest.raises(ValueError, match="does not exist"):
        courses.add("CS102", "Data Structures", 5, ["CS404"])
    with pytest.raises(ValueError, match="own prerequisite"):
        courses.add("CS102", "Data Structures", 5, ["CS102"])

    courses.add("CS102", "Data Structures", 5, ["CS101"])
    assert courses.has_dependents("CS101")
    with pytest.raises(ValueError, match="prerequisite for CS102"):
        courses.remove("CS101")

    courses.remove("CS102")
    courses.remove("CS101")
    assert CourseService(storage).all() == []


def test_course_service_skips_malformed_rows_and_normalizes_legacy_records(tmp_path):
    storage = JsonStorage(str(tmp_path))
    storage.save("courses.json", [
        None,
        {"code": "cs101", "name": " Intro ", "capacity": "3",
         "prerequisites": "not-a-list"},
        {"course_code": "CS102", "title": "Bad capacity", "capacity": "many"},
    ])

    courses = CourseService(storage)
    assert courses.all() == [{
        "course_code": "CS101",
        "title": "Intro",
        "name": "Intro",
        "capacity": 3,
        "prerequisites": [],
        "enrolled": [],
    }]
