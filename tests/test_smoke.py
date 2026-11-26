"""Headless smoke test — run with: pytest -q"""

import tempfile

from storage.json_storage import JsonStorage
from data_structures.structures import (
    StudentCollection, CourseCollection, EnrollmentCollection,
)
from services.student_service import StudentService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService


def _make_services(tmpdir):
    storage = JsonStorage(tmpdir)
    ss = StudentService(storage, StudentCollection([]))
    cs = CourseService(storage, CourseCollection([]))
    es = EnrollmentService(storage, EnrollmentCollection([]), ss, cs)
    return ss, cs, es


def test_prereq_and_capacity_rules():
    with tempfile.TemporaryDirectory() as tmp:
        ss, cs, es = _make_services(tmp)
        cs.add("CS101", "Intro", 2, [])
        cs.add("CS102", "Data Structures", 1, ["CS101"])
        ss.add("S1", "Alice", "a@x.com", ["CS101"])
        ss.add("S2", "Bob", "b@x.com", [])

        es.enroll("S1", "CS102")
        assert es.count_for_course("CS102") == 1

        # duplicate
        try:
            es.enroll("S1", "CS102")
            assert False, "duplicate should fail"
        except ValueError:
            pass

        # prerequisite missing
        try:
            es.enroll("S2", "CS102")
            assert False, "prereq should fail"
        except ValueError as e:
            assert "Prerequisite" in str(e)