# Test file for sorting.py
from algorithms.sorting import bubble_sort_by_name, bubble_sort_courses_by_capacity

# Test 1: Sort students by name
students = [
    {"name": "Pedro Garcia"},
    {"name": "Maria Santos"},
    {"name": "Juan Dela Cruz"},
]
sorted_students = bubble_sort_by_name(students)
print("Sorted by name:")
for s in sorted_students:
    print(" -", s["name"])
# dapat lumabas: Juan, Maria, Pedro (alphabetical order)

# Test 2: Sort courses by capacity
courses = [
    ("CS101", {"capacity": 30}),
    ("CS102", {"capacity": 10}),
    ("CS201", {"capacity": 20}),
]
sorted_courses = bubble_sort_courses_by_capacity(courses)
print("Sorted by capacity:")
for code, info in sorted_courses:
    print(" -", code, info["capacity"])
# dapat lumabas: CS102 (10), CS201 (20), CS101 (30)