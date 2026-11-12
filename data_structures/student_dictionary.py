# STUDENT DICTIONARY
# This file stores all student records.

class StudentDictionary:
    def __init__(self):
        self.students = {}

    def add_student(self, student_id, name):
        if student_id in self.students:
            return False
        self.students[student_id] = {
            "name": name,
            "completed_courses": set()
        }
        return True

    def get_student(self, student_id):
        return self.students.get(student_id)

    def student_exist(self, student_id):
        return student_id in self.students

    def add_completed_course(self, student_id, course_code):
        student = self.students.get(student_id)
        if student is None:
            return False 
        student["completed_courses"].add(course_code)
        return True

    def has_completed(self, student_id, course_code):
        student = self.students.get(student_id)
        if student is None:
            return False
        return course_code in student["completed_courses"]

    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            return True
        return False

    def get_all_student(self):
        return self.students