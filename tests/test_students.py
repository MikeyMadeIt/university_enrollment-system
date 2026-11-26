import tempfile

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
        assert StudentService(storage).get("S1")["completed_courses"] == ["CS101"]
