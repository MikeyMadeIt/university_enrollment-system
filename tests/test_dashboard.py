import importlib
import sys
import types

from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from storage.json_storage import JsonStorage


class FakeWidget:
    instances = []

    def __init__(self, master=None, **options):
        self.master = master
        self.options = options
        self.instances.append(self)

    def pack(self, **_options):
        pass

    def grid(self, **_options):
        pass

    def grid_columnconfigure(self, *_args, **_options):
        pass


def test_dashboard_displays_the_current_student_count(tmp_path, monkeypatch):
    storage = JsonStorage(str(tmp_path))
    students = StudentService(storage)
    courses = CourseService(storage)
    enrollments = EnrollmentService(storage, students, courses)
    students.add("S001", "Alice")

    fake_tkinter = types.ModuleType("tkinter")
    fake_tkinter.Frame = FakeWidget
    fake_tkinter.Label = FakeWidget
    monkeypatch.setitem(sys.modules, "tkinter", fake_tkinter)
    previous_module = sys.modules.pop("ui.pages.dashboard", None)

    try:
        dashboard_module = importlib.import_module("ui.pages.dashboard")
        FakeWidget.instances.clear()
        dashboard_module.Dashboard(object(), students, courses, enrollments)

        labels = [widget.options.get("text") for widget in FakeWidget.instances]
        assert "Total Students" in labels
        assert "1" in labels
    finally:
        sys.modules.pop("ui.pages.dashboard", None)
        if previous_module is not None:
            sys.modules["ui.pages.dashboard"] = previous_module
