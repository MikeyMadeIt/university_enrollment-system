# Test file for topological_sort.py
from algorithms.topological_sort import topological_sort

graph = {
    "CS101": ["CS102"],
    "CS102": ["CS201"],
    "CS201": [],
}

result = topological_sort(graph)
print("Valid course order:", result)
# dapat: CS101 muna, tapos CS102, tapos CS201 (ganito ang pagkakasunod kung i-take)