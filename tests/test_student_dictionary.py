# TEST FILE for student_dictionary.py
from data_structures.student_dictionary import StudentDictionary
sd = StudentDictionary()

sd.add_student("26-0001", "Denver Mapalo")
sd.add_student("26-0002", "Jhan Rackwell Tejada")
sd.add_student("26-0003", "Aryhana Gelicame")

# TEST 1: Add a new student
result = sd.add_student("26-0004", "Michael Ricamata")
print("Add student: ", result) # dapat True

# TEST 2: Add duplicate student (hindi dapat madadagdag)
result = sd.add_student("26-0004", "Michael Ricamata")
print("Add student: ", result) # dapat False

# TEST 3: Get student info
student = sd.get_student("26-0004")
print("Get student: ", student) 

# TEST 4: Check if student exists
print("Student exists (Real Id): ", sd.student_exist("26-0004")) # dapat True
print("Student exists (Fake Id): ", sd.student_exist("26-0005")) # dapat False

# TEST 5: Add completed course
sd.add_completed_course("26-0004", "CC101")
sd.add_completed_course("26-0004", "CC102")
print("Has completed: ", sd.get_student("26-0004")["completed_courses"])

# TEST 6: Check has_completed
print("Has completed: ", sd.has_completed("26-0004", "CC101")) # dapat True
print("Has completed: ", sd.has_completed("26-0004", "CC105")) # dapat False

# TEST 7: Get all student
print("All student: ", sd.get_all_student())

# TEST 8: Delete student
removed = sd.delete_student("26-0003")
print("Remove student: ", removed) # dapat True
print("All students after remove: ", sd.get_all_student()) 