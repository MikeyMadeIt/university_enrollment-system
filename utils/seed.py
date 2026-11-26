"""Seeds demo data on first run if the JSON files are missing/empty."""

import os

SEED_STUDENTS = [
    {"student_id": "S001", "name": "Alice Johnson", "email": "alice@uni.edu",
     "completed_courses": ["CS101"]},
    {"student_id": "S002", "name": "Bob Smith", "email": "bob@uni.edu",
     "completed_courses": []},
    {"student_id": "S003", "name": "Carol Lee", "email": "carol@uni.edu",
     "completed_courses": ["CS101", "MA101"]},
]

SEED_COURSES = [
    {"course_code": "CS101", "title": "Intro to Programming", "capacity": 30, "prerequisites": []},
    {"course_code": "MA101", "title": "Calculus I", "capacity": 40, "prerequisites": []},
    {"course_code": "CS102", "title": "Data Structures", "capacity": 25, "prerequisites": ["CS101"]},
    {"course_code": "CS201", "title": "Algorithms", "capacity": 20, "prerequisites": ["CS102", "MA101"]},
]

SEED_ENROLLMENTS = [
    {"student_id": "S001", "course_code": "CS102"},
    {"student_id": "S002", "course_code": "CS101"},
    {"student_id": "S003", "course_code": "MA101"},
]


def _needs_seed(path):
    return (not os.path.exists(path)) or os.path.getsize(path) == 0


def ensure_seed_data(storage):
    if _needs_seed(os.path.join(storage.base_dir, "students.json")):
        storage.save("students.json", SEED_STUDENTS)
    if _needs_seed(os.path.join(storage.base_dir, "courses.json")):
        storage.save("courses.json", SEED_COURSES)
    if _needs_seed(os.path.join(storage.base_dir, "enrollments.json")):
        storage.save("enrollments.json", SEED_ENROLLMENTS)