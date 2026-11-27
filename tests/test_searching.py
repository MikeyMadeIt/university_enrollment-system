# Test file for searching.py
from algorithms.searching import linear_search_by_name, linear_search_by_id, search_courses_by_keyword

# Sample data (parang galing sa StudentDictionary.get_all_students().values())
students = [
    {"name": "Maria Santos"},
    {"name": "Juan Dela Cruz"},
    {"name": "Pedro Garcia"},
]

# Test 1: Search by name na meron
result = linear_search_by_name(students, "Juan Dela Cruz")
print("Search found:", result)  # dapat lumabas yung dict ni Juan

# Test 2: Search by name na wala
result = linear_search_by_name(students, "Wala Dito")
print("Search not found:", result)  # dapat None

# Test 3: linear_search_by_id (dictionary lookup)
students_dict = {"2026-001": {"name": "Maria Santos"}}
result = linear_search_by_id(students_dict, "2026-001")
print("Search by id:", result)

# Test 4: Search courses by keyword
courses = {
    "CS101": {"name": "Intro to Programming"},
    "CS102": {"name": "Data Structures"},
    "CS201": {"name": "Advanced Programming"},
}
result = search_courses_by_keyword(courses, "Programming")
print("Search courses by keyword:", result)  # dapat 2 courses lumabas