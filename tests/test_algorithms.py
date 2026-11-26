from algorithms.bfs import bfs, bfs_levels
from algorithms.dfs import dfs
from algorithms.prerequisite_graph import build_prerequisite_graph
from algorithms.searching import linear_search_by_id, linear_search_by_name, search_courses_by_keyword
from algorithms.sorting import bubble_sort, merge_sort
from algorithms.topological_sort import topological_sort


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
    rows = [{"name": "Zed"}, {"name": "Amy"}]
    assert [row["name"] for row in bubble_sort(rows, "name")] == ["Amy", "Zed"]
    caps = [{"capacity": 30}, {"capacity": 10}, {"capacity": 20}]
    assert [row["capacity"] for row in merge_sort(caps, "capacity")] == [10, 20, 30]
