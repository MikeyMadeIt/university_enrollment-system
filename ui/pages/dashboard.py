import tkinter as tk
from tkinter import ttk
from services.student_service import StudentService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self._build_page()

    def _build_page(self):
        self.student_service = StudentService()
        self.course_service = CourseService()
        self.enrollment_service = EnrollmentService(
            student_service=self.student_service,
            course_service=self.course_service,
        )
        self.frame = tk.Frame(self.parent, bg="#F1F3F5")
        self.frame.pack(fill="both", expand=True)
        self.create_header()
        self.create_stats()
        self.create_capacity_table()

    def create_header(self):
        top = tk.Frame(self.frame, bg="#F1F3F5")
        top.pack(fill="x", padx=25, pady=(25, 15))
        tk.Label(
            top, text="Dashboard", font=("Arial", 22, "bold"),
            bg="#F1F3F5", fg="#07549C"
        ).pack(side="left")
        tk.Button(top, text="Refresh", command=self.refresh,
                  bg="#07549C", fg="white", relief="flat",
                  padx=16, pady=7).pack(side="right")

    def refresh(self):
        self.frame.destroy()
        self._build_page()

    def create_stats(self):
        stats_frame = tk.Frame(self.frame, bg="#F1F3F5")
        stats_frame.pack(fill="x", padx=25, pady=(0, 20))

        summary = {
            "Total Students": len(self.student_service.get_all_students()),
            "Total Courses": len(self.course_service.get_all_courses()),
            "Total Enrollments": len(self.enrollment_service.get_all_records()),
        }

        for title, value in summary.items():
            card = tk.Frame(
                stats_frame, bg="#FFFFFF", padx=20, pady=15,
                highlightbackground="#D9DDE2", highlightthickness=1
            )
            card.pack(side="left", fill="both", expand=True, padx=(0, 15))
            tk.Label(
                card, text=title, font=("Arial", 11),
                fg="#555555", bg="#FFFFFF"
            ).pack(anchor="w")
            tk.Label(
                card, text=str(value), font=("Arial", 24, "bold"),
                fg="#333333", bg="#FFFFFF"
            ).pack(anchor="w", pady=(8, 0))

    def create_capacity_table(self):
        tk.Label(
            self.frame, text="Courses Approaching Capacity",
            font=("Arial", 14, "bold"), bg="#F1F3F5", fg="#07549C"
        ).pack(anchor="w", padx=25, pady=(10, 10))

        tf = tk.Frame(self.frame, bg="white", relief="solid", bd=1)
        tf.pack(fill="both", expand=True, padx=25, pady=(0, 25))

        self.tree = ttk.Treeview(tf, columns=("code", "name", "enroll"), show="headings", height=8)
        self.tree.heading("code", text="Course Code")
        self.tree.heading("name", text="Course Name")
        self.tree.heading("enroll", text="Enrollment")
        self.tree.column("code", width=150, anchor="center")
        self.tree.column("name", width=400, anchor="w")
        self.tree.column("enroll", width=150, anchor="center")

        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", padx=(0, 10), pady=10)

        courses = self.course_service.get_all_courses()
        # Calculate fill percentage and sort descending
        course_list = []
        for code, info in courses.items():
            enrolled_count = len(info["enrolled"])
            capacity = info["capacity"]
            if capacity > 0:
                fill_pct = enrolled_count / capacity
                course_list.append((fill_pct, code, info["name"], f"{enrolled_count}/{capacity}"))

        course_list.sort(key=lambda x: x[0], reverse=True)

        # Show top 5 closest to capacity
        for item in course_list[:5]:
            self.tree.insert("", "end", values=(item[1], item[2], item[3]))
