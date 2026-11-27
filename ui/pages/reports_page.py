import tkinter as tk
from services.student_service import StudentService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from services.report_service import ReportService


class ReportsPage:
    def __init__(self, parent):
        self.parent = parent
        self.student_service = StudentService()
        self.course_service = CourseService()
        self.enrollment_service = EnrollmentService(
            student_service=self.student_service,
            course_service=self.course_service)
        self.report_service = ReportService(
            self.enrollment_service, self.student_service, self.course_service)
        self.frame = tk.Frame(parent, bg="#F1F3F5")
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="Reports & Algorithm Demos",
                 font=("Arial", 22, "bold"), bg="#F1F3F5", fg="#07549C"
                 ).pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame,
                 text="CSV exports and live demonstrations of the self-implemented algorithms",
                 font=("Arial", 10), bg="#F1F3F5", fg="#555555"
                 ).pack(anchor="w", padx=25)

        s = self.report_service.summary()
        tk.Label(self.frame,
                 text=f"Students: {s['total_students']}    "
                      f"Courses: {s['total_courses']}    "
                      f"Enrollments: {s['total_enrollments']}",
                 font=("Arial", 11, "bold"), bg="#F1F3F5", fg="#333"
                 ).pack(anchor="w", padx=25, pady=15)

        btn_frame = tk.Frame(self.frame, bg="#F1F3F5")
        btn_frame.pack(fill="x", padx=25, pady=5)
        for label, cmd in [
            ("Export Enrollments CSV", self._export_enrollments),
            ("Export Students CSV", self._export_students),
            ("Export Courses CSV", self._export_courses),
            ("Export All", self._export_all),
        ]:
            tk.Button(btn_frame, text=label, bg="#07549C", fg="white",
                      relief="flat", padx=15, pady=8, command=cmd
                      ).pack(side="left", padx=(0, 8))

        self.result = tk.Label(self.frame, text="", font=("Arial", 10),
                                bg="#F1F3F5", fg="#16803C")
        self.result.pack(anchor="w", padx=25, pady=10)

        demo = tk.Frame(self.frame, bg="#F1F3F5")
        demo.pack(fill="both", expand=True, padx=25, pady=(10, 20))

        left = tk.Frame(demo, bg="white", padx=15, pady=10)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(left, text="Students — bubble_sort_by_name",
                 font=("Arial", 11, "bold"), bg="white", fg="#07549C"
                 ).pack(anchor="w")
        for sid, info in self.student_service.sorted_students():
            tk.Label(left, text=f"  {sid}  {info['name']}",
                     font=("Consolas", 9), bg="white", anchor="w"
                     ).pack(fill="x")
        tk.Label(left, text="Courses — bubble_sort_courses_by_capacity",
                 font=("Arial", 11, "bold"), bg="white", fg="#07549C"
                 ).pack(anchor="w", pady=(15, 0))
        for code, info in self.course_service.sorted_courses():
            tk.Label(left,
                     text=f"  {code}  {info['name']}  cap={info['capacity']}",
                     font=("Consolas", 9), bg="white", anchor="w"
                     ).pack(fill="x")

        right = tk.Frame(demo, bg="white", padx=15, pady=10)
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))
        tk.Label(right, text="Topological order — topological_sort",
                 font=("Arial", 11, "bold"), bg="white", fg="#07549C"
                 ).pack(anchor="w")
        order = self.course_service.topological_order()
        text = " → ".join(order) if order else "(cycle detected)"
        tk.Label(right, text=text, font=("Consolas", 9), bg="white",
                 wraplength=400, justify="left", anchor="w"
                 ).pack(fill="x")

        courses = list(self.course_service.get_all_courses().keys())
        if courses:
            sample = courses[0]
            tk.Label(right,
                     text=f"BFS levels from {sample} — bfs_levels",
                     font=("Arial", 11, "bold"), bg="white", fg="#07549C"
                     ).pack(anchor="w", pady=(15, 0))
            for c, lvl in self.course_service.bfs_levels_from(sample).items():
                tk.Label(right, text=f"  L{lvl}: {c}",
                         font=("Consolas", 9), bg="white", anchor="w"
                         ).pack(fill="x")

            tk.Label(right,
                     text=f"DFS from {sample} — dfs",
                     font=("Arial", 11, "bold"), bg="white", fg="#07549C"
                     ).pack(anchor="w", pady=(15, 0))
            tk.Label(right,
                     text=" → ".join(
                         self.course_service.dfs_dependents(sample)),
                     font=("Consolas", 9), bg="white", wraplength=400,
                     justify="left", anchor="w").pack(fill="x")

    def _export_enrollments(self):
        p = self.report_service.export_enrollments_csv()
        self.result.config(text=f"Saved: {p}", fg="#16803C")

    def _export_students(self):
        p = self.report_service.export_students_csv()
        self.result.config(text=f"Saved: {p}", fg="#16803C")

    def _export_courses(self):
        p = self.report_service.export_courses_csv()
        self.result.config(text=f"Saved: {p}", fg="#16803C")

    def _export_all(self):
        paths = self.report_service.export_all()
        self.result.config(
            text="Saved: " + ", ".join(str(p) for p in paths.values()),
            fg="#16803C")
