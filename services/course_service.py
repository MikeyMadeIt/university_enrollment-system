"""Course operations backed by CourseDictionary and prerequisite algorithms."""

from algorithms.prerequisite_graph import build_prerequisite_graph
from algorithms.searching import search_courses_by_keyword
from algorithms.topological_sort import topological_sort
from data_structures.course_dictionary import CourseDictionary


class CourseService:
    def __init__(self, storage):
        self.storage = storage
        self.courses = CourseDictionary()
        for row in storage.load("courses.json", []):
            code = row.get("course_code", row.get("code"))
            title = row.get("title", row.get("name", ""))
            if code and title:
                self.courses.add_course(str(code).upper(), title, int(row.get("capacity", 0)),
                                         row.get("prerequisites", []))

    def add(self, code, title, capacity, prerequisites=None):
        code, title = (code or "").strip().upper(), (title or "").strip()
        if not code or not title:
            raise ValueError("Course code and title are required")
        try:
            capacity = int(capacity)
        except (TypeError, ValueError) as exc:
            raise ValueError("Capacity must be an integer") from exc
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        prereqs = list(dict.fromkeys(str(p).strip().upper() for p in (prerequisites or []) if str(p).strip()))
        if code in prereqs:
            raise ValueError("A course cannot be its own prerequisite")
        for prereq in prereqs:
            if not self.courses.course_exists(prereq):
                raise ValueError(f"Prerequisite course {prereq} does not exist")
        if not self.courses.add_course(code, title, capacity, prereqs):
            raise ValueError(f"Course {code} already exists or capacity is invalid")
        self._persist()
        return self.get(code)

    def remove(self, code):
        code = (code or "").strip().upper()
        if not self.courses.course_exists(code):
            raise ValueError(f"Course {code} not found")
        for dependent, course in self.courses.get_all_courses().items():
            if dependent != code and code in course["prerequisites"]:
                raise ValueError(f"Course {code} is a prerequisite for {dependent}")
        if self.courses.get_course(code)["enrolled"]:
            raise ValueError(f"Course {code} still has enrolled students")
        # The original CourseDictionary has no delete method; removal from its
        # authoritative mapping is the only available operation.
        del self.courses.courses[code]
        self._persist()

    def has_dependents(self, code):
        code = (code or "").strip().upper()
        return any(dependent != code and code in course["prerequisites"]
                   for dependent, course in self.courses.get_all_courses().items())

    def get(self, code):
        code = (code or "").strip().upper()
        row = self.courses.get_course(code)
        if row is None:
            return None
        return {"course_code": code, "title": row["name"], "name": row["name"],
                "capacity": row["capacity"], "prerequisites": list(row["prerequisites"]),
                "enrolled": list(row["enrolled"])}

    def all(self):
        return [self.get(code) for code in self.courses.get_all_courses()]

    def search(self, keyword):
        keyword = (keyword or "").strip()
        if not keyword:
            return []
        return [{**course, "course_code": code} for code, course in
                search_courses_by_keyword(self.courses.get_all_courses(), keyword)]

    def prerequisite_graph(self):
        return build_prerequisite_graph(self.courses.get_all_courses())

    def prerequisite_order(self):
        return topological_sort(self.prerequisite_graph())

    def _persist(self):
        self.storage.save("courses.json", [
            {"course_code": c["course_code"], "title": c["title"],
             "capacity": c["capacity"], "prerequisites": c["prerequisites"]}
            for c in self.all()
        ])
