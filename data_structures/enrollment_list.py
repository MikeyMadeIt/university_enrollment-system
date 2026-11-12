# ENROLLMENT LIST
# This file keeps a list (log) of all enrollment transactions.

class EnrollmentList:
    def __init__(self):
        self.records = []

    def add_record(self, student_id, course_code, timestamp=None):
        record = {
            "student_id": student_id,
            "course_code": course_code,
            "timestamp": timestamp
        }
        self.records.append(record)
        return record

    def get_all_records(self):
        return self.records

    def filter_by_student(self, student_id):
        result = []
        for record in self.records:
            if record["student_id"] == student_id:
                result.append(record)
        return result

    def filter_by_course(self, course_code):
        result = []
        for record in self.records:
            if record["course_code"] == course_code:
                result.append(record)
        return result