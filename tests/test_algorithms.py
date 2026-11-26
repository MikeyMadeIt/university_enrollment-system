from algorithms import (
    bfs,
    bfs_levels,
    bubble_sort_by_name,
    bubble_sort_courses_by_capacity,
    build_prerequisite_graph,
    dfs,
    linear_search_by_id,
    linear_search_by_name,
    search_courses_by_keyword,
    topological_sort,
)
import algorithms.sorting as sorting
from data_structures import CourseDictionary, EnrollmentList, EnrollmentSet, StudentDictionary


def test_graph_traversals_and_course_order():
    courses = {
        "CS101": {"prerequisites": set()},
        "CS102": {"prerequisites": {"CS101"}},
        "CS201": {"prerequisites": {"CS102"}},
    }
    graph = build_prerequisite_graph(courses)
    assert graph == {"CS101": ["CS102"], "CS102": ["CS201"], "CS201": []}
    assert dfs(graph, "CS101") == ["CS101", "CS102", "CS201"]
    assert bfs(graph, "CS101") == ["CS101", "CS102", "CS201"]
    assert bfs_levels(graph, "CS101") == {"CS101": 0, "CS102": 1, "CS201": 2}
    order = topological_sort(graph)
    assert order.index("CS101") < order.index("CS102") < order.index("CS201")


def test_original_search_and_sort_functions():
    students = [{"id": "S1", "name": "Alice"}, {"id": "S2", "name": "Bob"}]
    assert linear_search_by_name(students, "bob")["id"] == "S2"
    assert linear_search_by_id({"S1": students[0]}, "S1")["name"] == "Alice"
    courses = {"CS101": {"name": "Intro Programming"}, "MA101": {"name": "Math"}}
    assert search_courses_by_keyword(courses, "programming")[0][0] == "CS101"
    rows = [{"name": "Zed"}, {"name": "amy"}]
    assert [row["name"] for row in bubble_sort_by_name(rows)] == ["amy", "Zed"]
    assert [row["name"] for row in rows] == ["Zed", "amy"]

    courses = [
        ("CS101", {"capacity": 30}),
        ("CS102", {"capacity": 10}),
        ("CS201", {"capacity": 20}),
    ]
    assert [code for code, _ in bubble_sort_courses_by_capacity(courses)] == [
        "CS102", "CS201", "CS101"
    ]
    assert {
        name for name in vars(sorting)
        if name.startswith("bubble_sort")
    } == {"bubble_sort_by_name", "bubble_sort_courses_by_capacity"}


def test_data_structure_package_exports():
    students = StudentDictionary()
    courses = CourseDictionary()
    enrollments = EnrollmentSet()
    records = EnrollmentList()

    assert students.add_student("S1", "Ada")
    assert courses.add_course("CS101", "Programming", 10)
    assert enrollments.add_enrollment("S1", "CS101")
    assert records.add_record("S1", "CS101")["student_id"] == "S1"
