import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _class_method(tree, class_name, method_name):
    cls = next(node for node in tree.body
               if isinstance(node, ast.ClassDef) and node.name == class_name)
    return next(node for node in cls.body
                if isinstance(node, ast.FunctionDef) and node.name == method_name)


def test_sidebar_pages_route_to_the_expected_services():
    sidebar_tree = ast.parse((ROOT / "ui/components/sidebar.py").read_text())
    sidebar_class = next(node for node in sidebar_tree.body
                         if isinstance(node, ast.ClassDef) and node.name == "Sidebar")
    pages_assignment = next(node for node in sidebar_class.body
                            if isinstance(node, ast.Assign)
                            and any(isinstance(target, ast.Name) and target.id == "PAGES"
                                    for target in node.targets))
    page_names = ast.literal_eval(pages_assignment.value)

    main_tree = ast.parse((ROOT / "ui/main_window.py").read_text())
    show_page = _class_method(main_tree, "MainWindow", "show_page")
    routed_calls = {}
    for node in ast.walk(show_page):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            routed_calls[node.func.id] = [ast.unparse(arg) for arg in node.args]

    expected_routes = {
        "Dashboard": ["self.page_container", "self.student_service", "self.course_service",
                      "self.enrollment_service"],
        "StudentsPage": ["self.page_container", "self.student_service",
                          "self.enrollment_service", "self.course_service"],
        "CoursesPage": ["self.page_container", "self.course_service",
                         "self.enrollment_service", "self.student_service"],
        "EnrollmentsPage": ["self.page_container", "self.student_service",
                            "self.course_service", "self.enrollment_service"],
        "RecordsPage": ["self.page_container", "self.enrollment_service",
                        "self.student_service", "self.course_service"],
    }
    assert page_names == ["Dashboard", "Students", "Courses", "Enrollments", "Records"]
    for page_class, arguments in expected_routes.items():
        assert routed_calls[page_class] == arguments
