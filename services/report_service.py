import csv
from pathlib import Path


class ReportService:
    def __init__(self, enrollment_service, student_service, course_service,
                 export_dir="exports"):
        self.enrollment_service = enrollment_service
        self.student_service = student_service
        self.course_service = course_service
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def summary(self):
        return {
            "total_students": len(self.student_service.get_all_students()),
            "total_courses": len(self.course_service.get_all_courses()),
            "total_enrollments": len(self.enrollment_service.get_all_records()),
        }

    def export_enrollments_csv(self, filename="enrollments.csv"):
        path = self.export_dir / filename
        records = self.enrollment_service.get_all_records()
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["student_id", "student_name",
                                              "course_code", "course_name",
                                              "timestamp"])
            w.writeheader()
            w.writerows(records)
        return path

    def export_students_csv(self, filename="students.csv"):
        path = self.export_dir / filename
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["student_id", "name", "completed_courses"])
            for sid, info in self.student_service.sorted_students():
                w.writerow([sid, info["name"],
                            ",".join(sorted(info["completed_courses"]))])
        return path

    def export_courses_csv(self, filename="courses.csv"):
        path = self.export_dir / filename
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["code", "name", "capacity", "enrolled_count",
                        "prerequisites"])
            for code, info in self.course_service.sorted_courses():
                w.writerow([code, info["name"], info["capacity"],
                            len(info["enrolled"]),
                            ",".join(sorted(info["prerequisites"]))])
        return path

    def export_all(self):
        return {
            "enrollments": self.export_enrollments_csv(),
            "students": self.export_students_csv(),
            "courses": self.export_courses_csv(),
        }
