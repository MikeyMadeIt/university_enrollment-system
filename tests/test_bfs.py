# Test file for bfs.py
from algorithms.bfs import bfs, bfs_levels

graph = {
    "CS101": ["CS102"],
    "CS102": ["CS201", "CS202"],
    "CS201": [],
    "CS202": [],
}

result = bfs(graph, "CS101")
print("BFS result:", result)

levels = bfs_levels(graph, "CS101")
print("BFS levels:", levels)
# dapat: CS101 = 0, CS102 = 1, CS201 = 2, CS202 = 2