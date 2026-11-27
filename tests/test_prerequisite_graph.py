# Test file for prerequisite_graph.py
from algorithms.prerequisite_graph import build_prerequisite_graph

courses = {
    "CS101": {"name": "Intro", "prerequisites": set()},
    "CS102": {"name": "Data Structures", "prerequisites": {"CS101"}},
    "CS201": {"name": "Algorithms", "prerequisites": {"CS102"}},
}

graph = build_prerequisite_graph(courses)
print("Graph:", graph)
# dapat lumabas: CS101 -> [CS102], CS102 -> [CS201], CS201 -> []