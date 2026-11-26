"""Validated collection wrappers (dict/set/list based)."""


class StudentCollection:
    """Dictionary keyed by student_id -> student dict."""

    def __init__(self, students=None):
        self._items = {}
        for s in students or []:
            self.add(s)

    def add(self, student):
        sid = student["student_id"]
        if sid in self._items:
            raise ValueError(f"Student ID {sid} already exists")
        self._items[sid] = student

    def get(self, sid):
        return self._items.get(sid)

    def all(self):
        return list(self._items.values())

    def remove(self, sid):
        return self._items.pop(sid, None) is not None

    def __len__(self):
        return len(self._items)


class CourseCollection:
    """Dictionary keyed by course_code -> course dict."""

    def __init__(self, courses=None):
        self._items = {}
        for c in courses or []:
            self.add(c)

    def add(self, course):
        code = course["course_code"]
        if code in self._items:
            raise ValueError(f"Course {code} already exists")
        self._items[code] = course

    def get(self, code):
        return self._items.get(code)

    def all(self):
        return list(self._items.values())

    def remove(self, code):
        return self._items.pop(code, None) is not None

    def __len__(self):
        return len(self._items)


class EnrollmentCollection:
    """List of enrollments, plus a set index to enforce uniqueness."""

    def __init__(self, enrollments=None):
        self._items = []
        self._index = set()
        for e in enrollments or []:
            self.add(e)

    def add(self, enrollment):
        key = (enrollment["student_id"], enrollment["course_code"])
        if key in self._index:
            raise ValueError(f"Enrollment already exists: {key}")
        self._items.append(enrollment)
        self._index.add(key)

    def remove(self, student_id, course_code):
        key = (student_id, course_code)
        if key not in self._index:
            return False
        self._items = [
            e for e in self._items
            if (e["student_id"], e["course_code"]) != key
        ]
        self._index.discard(key)
        return True

    def exists(self, student_id, course_code):
        return (student_id, course_code) in self._index

    def count_for_course(self, course_code):
        return sum(1 for e in self._items if e["course_code"] == course_code)

    def for_student(self, student_id):
        return [e for e in self._items if e["student_id"] == student_id]

    def for_course(self, course_code):
        return [e for e in self._items if e["course_code"] == course_code]

    def all(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)