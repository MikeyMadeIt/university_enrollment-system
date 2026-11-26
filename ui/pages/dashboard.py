import tkinter as tk
from tkinter import ttk

from algorithms.sorting import bubble_sort


BLUE, PAGE, WHITE = "#07549C", "#F1F3F5", "#FFFFFF"


class Dashboard:
    def __init__(self, parent, student_service, course_service, enrollment_service):
        self.parent = parent
        self.students, self.courses, self.enrollments = student_service, course_service, enrollment_service
        self.frame = tk.Frame(parent, bg=PAGE)
        self.frame.pack(fill="both", expand=True)
        self.create_header()
        self.create_statistics()
        self.create_capacity_section()

    def create_header(self):
        tk.Label(self.frame, text="Dashboard", font=("Arial", 22, "bold"),
                 bg=PAGE, fg=BLUE).pack(anchor="w", padx=25, pady=20)

    def create_statistics(self):
        stats = tk.Frame(self.frame, bg=PAGE)
        stats.pack(fill="x", padx=25, pady=10)
        values = (("Total Students", len(self.students.all())),
                  ("Total Courses", len(self.courses.all())),
                  ("Total Enrollments", len(self.enrollments.all())))
        for index, (title, value) in enumerate(values):
            card = tk.Frame(stats, bg=WHITE, padx=20, pady=15,
                            highlightbackground="#D9DDE2", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True,
                      padx=(0 if index == 0 else 10, 0 if index == 2 else 10))
            tk.Label(card, text=title, font=("Arial", 11), fg="#555555", bg=WHITE).pack(anchor="w")
            tk.Label(card, text=str(value), font=("Arial", 24, "bold"),
                     fg="#333333", bg=WHITE).pack(anchor="w", pady=(8, 0))

    def create_capacity_section(self):
        panel = tk.Frame(self.frame, bg=WHITE, highlightbackground="#D9DDE2", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=25, pady=20)
        tk.Label(panel, text="Courses Approaching Capacity", font=("Arial", 14, "bold"),
                 fg=BLUE, bg=WHITE).pack(anchor="w", padx=20, pady=15)
        columns = ("course_code", "course_name", "enrollment")
        tree = ttk.Treeview(panel, columns=columns, show="headings", height=10)
        for col, title, width in (("course_code", "Course Code", 150),
                                  ("course_name", "Course Name", 380),
                                  ("enrollment", "Enrollment", 150)):
            tree.heading(col, text=title)
            tree.column(col, width=width, anchor="w")
        tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        rows = []
        for course in self.courses.all():
            count = self.enrollments.count_for_course(course["course_code"])
            capacity = course["capacity"]
            if capacity and count / capacity >= 0.8:
                rows.append({"course_code": course["course_code"], "title": course["title"],
                             "enrollment": f"{count}/{capacity}"})
        for course in bubble_sort(rows, "course_code"):
            tree.insert("", "end", values=(course["course_code"], course["title"], course["enrollment"]))
