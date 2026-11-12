# TEST FILE for enrollment_list.py
from data_structures.enrollment_list import EnrollmentList 
el = EnrollmentList()

# TEST 1: Add records
record1 = el.add_record("26-0001", "CC101", "11-11-2026")
print("Add record 1: ", record1)

record2 = el.add_record("26-0001", "CC102", "11-12-2026")
print("Add record 2: ", record2)

record3 = el.add_record("26-0002", "CC101", "11-13-2026")
print("Add record 3: ", record3)

# TEST 2: Get all records (dapat sunod-sunod ayon sa pagkakadagdag)
print("All records: ", el.get_all_records())

# TEST 3: Filter by student
print("Filter by student: ", el.filter_by_student("26-0001")) # dapat 2 records

# TEST 4: Filter by student na wala
print("Filter by fake student: ", el.filter_by_student("26-9999")) # dapat empty list

# TEST 5: Filter by course
print("Filter by course: ", el.filter_by_course("CC101")) # dapat 2 records (26-0001 at 26-0002)

# TEST 6: Filter by course na wala
print("Filter by fake course: ", el.filter_by_course("CC999")) # dapat empty list