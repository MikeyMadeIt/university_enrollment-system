# COURSE DICTIONARY
# This file stores all course records.

class CourseDictionary:
    def __init__(self):
        self.courses = {}

    def add_course(self, course_code, name, capacity, prerequisites=None):
        if course_code in self.courses:
            return False 
        if prerequisites is None:
            prerequisites = []
        self.courses[course_code] = {
            "name": name,
            "capacity": capacity,
            "enrolled": set(),
            "prerequisites": set(prerequisites)
        }
        return True

    def get_course(self, course_code):
        return self.courses.get(course_code)

    def course_exists(self, course_code):
        return course_code in self.courses

    def has_slot(self, course_code):
        course = self.courses.get(course_code)
        if course is None:
            return False
        return len(course["enrolled"]) < course["capacity"]

    def enroll_student(self, course_code, student_id):
        course = self.courses.get(course_code)
        if course is None:
            return False
        if not self.has_slot(course_code):
            return False
        course["enrolled"].add(student_id)
        return True

    def drop_student(self, course_code, student_id):
        course = self.courses.get(course_code)
        if course is None:
            return False
        course["enrolled"].discard(student_id)
        return True
        
    def meets_prerequisites(self, course_code, completed_courses):
        course = self.courses.get(course_code)
        if course is None:
            return False
        for req in course["prerequisites"]:
            if req not in completed_courses:
                return False
        return True
            
    def get_all_courses(self):
        return self.courses