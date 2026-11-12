# TEST FILE for course_dictionary.py
from data_structures.course_dictionary import CourseDictionary 
cd = CourseDictionary()

# TEST 1: Add a new course
result = cd.add_course("CC101", "Intro to Programming", 2)
print("Add course: ", result) # dapat True 

# TEST 2: Add a new course with prerequisite
result = cd.add_course("CC102", "Data Structures & Algorithms", 2, ["CC101"])
print("Add course with prerequisite: ", cd.get_course("CC102"))

# TEST 3: Add duplicate course (dapat hindi na madagdag)
result = cd.add_course("CC101", "Intro to Programming", 2)
print("Add duplicate course: ", result) # dapat False

# TEST 4: Check course_exists
print("Course exists (Real Code): ", cd.course_exists("CC101")) # dapat True
print("Course exists (Fake Code): ", cd.course_exists("CC999")) # dapat False

# TEST 5: Check has_slot (dapat may slot pa, kasi 0 pa lang naka-enroll)
print("Has slot:", cd.has_slot("CC101")) # dapat True

# TEST 6: Enroll students hanggang mapuno
cd.enroll_student("CC101", "26-0001")
cd.enroll_student("CC101", "26-0002")
print("Has slot after full: ", cd.has_slot("CC101")) # dapat False (capacity 2, puno na)

# TEST 7: Try enroll even it is full
result = cd.enroll_student("CC101", "26-0003")
print("Enroll when full: ", result) # dapat False

# TEST 8: Drop a student
cd.drop_student("CC101", "26-0002")
print("Has slot after drop: ", cd.has_slot("CC101")) # dapat True

# TEST 9: Check meets_prerequisites
completed = {"CS101"}
print("Meets prereq CC102:", cd.meets_prerequisites("CC102", completed))  # dapat True

completed_wala = set()
print("Meets prereq CC102 (walang tapos):", cd.meets_prerequisites("CC102", completed_wala))  # dapat False

# TEST 10: Get all course
print("All course: ", cd.get_all_courses())