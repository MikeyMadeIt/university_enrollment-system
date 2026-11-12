# ENROLLMENT SET
# This file checks and prevents duplicate enrollment.

class EnrollmentSet:
    def __init__(self):
        self.enrollments = set()

    def is_duplicate(self, student_id, course_code):
        pair = (student_id, course_code)
        return pair in self.enrollments

    def add_enrollment(self, student_id, course_code):
        pair = (student_id, course_code)
        if pair in self.enrollments:
            return False
        self.enrollments.add(pair)
        return True

    def remove_enrollment(self, student_id, course_code):
        pair = (student_id, course_code)
        if pair in self.enrollments:
            self.enrollments.remove(pair)
            return True
        return False

    def get_courses_of_student(self, student_id):
        result = set()
        for (s_id, c_code) in self.enrollments:
            if s_id == student_id:
                result.add(c_code)
        return result

    def get_students_of_course(self, course_code):
        result = set()
        for (s_id, c_code) in self.enrollments:
            if c_code == course_code:
                result.add(s_id)
        return(result)