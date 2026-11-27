from storage.json_storage import JsonStorage
from utils.validation import validate_course_code, validate_name, validate_capacity
from data_structures.course_dictionary import CourseDictionary
from algorithms.searching import search_courses_by_keyword
from algorithms.sorting import bubble_sort_courses_by_capacity
from algorithms.prerequisite_graph import build_prerequisite_graph
from algorithms.dfs import dfs
from algorithms.bfs import bfs, bfs_levels
from algorithms.topological_sort import topological_sort


class CourseService:
    def __init__(self, storage=None):
        self.storage = storage or JsonStorage()
        self.dict = CourseDictionary()
        self._load()

    def _load(self):
        raw = self.storage.load_courses()
        for code, info in raw.items():
            self.dict.add_course(code, info["name"], info["capacity"],
                                 info.get("prerequisites", []))
            for sid in info.get("enrolled", []):
                self.dict.enroll_student(code, sid)

    def _save(self):
        raw = {}
        for code, info in self.dict.get_all_courses().items():
            raw[code] = {
                "name": info["name"],
                "capacity": info["capacity"],
                "enrolled": sorted(info["enrolled"]),
                "prerequisites": sorted(info["prerequisites"]),
            }
        self.storage.save_courses(raw)

    def reload(self):
        self.dict = CourseDictionary()
        self._load()

    def add_course(self, code, name, capacity, prerequisites=None):
        code = code.strip().upper()
        name = name.strip()
        if not validate_course_code(code):
            return False, "Invalid course code."
        if not validate_name(name):
            return False, "Invalid course name."
        if not validate_capacity(capacity):
            return False, "Capacity must be a positive integer."
        prereqs = [p.strip().upper() for p in (prerequisites or [])]
        if not self.dict.add_course(code, name, int(capacity), prereqs):
            return False, "Course code already exists."
        self._save()
        return True, "Course added successfully."

    def delete_course(self, code):
        code = code.strip().upper()
        course = self.dict.get_course(code)
        if course is None:
            return False, "Course not found."
        if course["enrolled"]:
            return False, "Drop all enrolled students before deleting this course."
        dependents = [
            other_code for other_code, info in self.dict.get_all_courses().items()
            if code in info["prerequisites"]
        ]
        if dependents:
            return False, "This course is a prerequisite for: " + ", ".join(
                sorted(dependents))
        del self.dict.courses[code]
        self._save()
        return True, "Course deleted."

    def get_all_courses(self):
        return self.dict.get_all_courses()

    def get_course(self, code):
        return self.dict.get_course(code.upper())

    # ---- searching (self-implemented) -------------------------
    def search_by_code(self, code):
        return self.dict.get_course(code.upper())

    def search_by_keyword(self, keyword):
        return search_courses_by_keyword(self.dict.get_all_courses(), keyword)

    # ---- sorting (self-implemented) ---------------------------
    def sorted_courses(self, by="capacity"):
        records = list(self.dict.get_all_courses().items())
        return bubble_sort_courses_by_capacity(records)

    # ---- graph (self-implemented) -----------------------------
    def _graph(self):
        return build_prerequisite_graph(self.dict.get_all_courses())

    def topological_order(self):
        return topological_sort(self._graph())

    def dfs_dependents(self, code):
        return dfs(self._graph(), code.upper())

    def bfs_levels_from(self, code):
        return bfs_levels(self._graph(), code.upper())

    # ---- capacity / prereq ------------------------------------
    def has_slot(self, code):
        return self.dict.has_slot(code.upper())

    def meets_prerequisites(self, code, completed):
        return self.dict.meets_prerequisites(code.upper(), set(completed))

    # ---- roster -----------------------------------------------
    def get_roster(self, code):
        course = self.dict.get_course(code.upper())
        if not course:
            return []
        return sorted(course["enrolled"])

    def add_enrollment(self, code, student_id):
        ok = self.dict.enroll_student(code.upper(), student_id)
        if ok:
            self._save()
        return ok

    def remove_enrollment(self, code, student_id):
        ok = self.dict.drop_student(code.upper(), student_id)
        if ok:
            self._save()
        return ok
