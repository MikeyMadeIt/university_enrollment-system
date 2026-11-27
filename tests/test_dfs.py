# Test file for dfs.py
from algorithms.dfs import dfs

graph = {
    "CS101": ["CS102"],
    "CS102": ["CS201", "CS202"],
    "CS201": [],
    "CS202": [],
}

result = dfs(graph, "CS101")
print("DFS result:", result)
# dapat ma-visit lahat ng courses na naaapektuhan ng CS101