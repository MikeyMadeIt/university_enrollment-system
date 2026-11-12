# TEST FILE for enrollment_set.py
from data_structures.enrollment_set import EnrollmentSet 
es = EnrollmentSet()

# TEST 1: Add a new student
result = es.add_enrollment("26-0001", "CC101")
print("Add enrollment: ", result) # dapat True

# TEST 2: Add duplicate enrollment
result = es.add_enrollment("26-0001", "CC101")
print("Add duplicate enrollment: ", result) # dapat False

# TEST 3: Check is_duplicate
print("Is duplicate: ", es.is_duplicate("26-0001", "CC101")) # dapat True
print("Is duplicate (walapa): ", es.is_duplicate("26-9999", "CC999")) # dapat False

# TEST 4: Add more enrollment
es.add_enrollment("26-0001", "CC102")
es.add_enrollment("26-0002", "CC101")
es.add_enrollment("26-0003", "CC101")

# TEST 5: Get courses of a student 
print("Courses of 2026-0001: ", es.get_courses_of_student("26-0001")) # dapat {"CC101", "CC102"}

# TEST 6: Get students of a course 
print("Students of CC101: ", es.get_students_of_course("CC101")) # {"26-0001", "26-0002", "26-0003"}

# TEST 7: Remove enrollment
remove = es.remove_enrollment("26-0001", "CC101")
print("Remove enrollment: ", remove)
print("Courses of 26-0001 after removed: ", es.get_courses_of_student("26-0001")) # dapat {"CC102"}

# TEST 8: Remove enrollment na wala naman
remove = es.remove_enrollment("26-9999", "CC999") 
print("Remove non-existing enrollment: ", remove) # dapat False