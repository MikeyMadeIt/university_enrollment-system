import tempfile

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
