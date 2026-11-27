import tkinter as tk
from tkinter import ttk
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from services.course_service import CourseService

class RecordsPage:
    def __init__(self, parent):
        self.parent = parent
        self.student_service = StudentService()
        self.course_service = CourseService()
        self.service = EnrollmentService(
            student_service=self.student_service,
            course_service=self.course_service,
        )
        self.frame = tk.Frame(parent, bg="#F1F3F5")
        self.frame.pack(fill="both", expand=True)
        self.create_header()
        self.create_table()
        self.refresh()

    def create_header(self):
        top = tk.Frame(self.frame, bg="#F1F3F5")
        top.pack(fill="x", padx=25, pady=(25, 5))
        tk.Label(
            top, text="Enrollment Records", font=("Arial", 22, "bold"),
            bg="#F1F3F5", fg="#07549C"
        ).pack(side="left")
        tk.Button(top, text="Refresh", command=self.refresh,
                  bg="#07549C", fg="white", relief="flat",
                  padx=16, pady=7).pack(side="right")

    def create_table(self):
        table_frame = tk.Frame(self.frame, bg="#FFFFFF")
        table_frame.pack(fill="both", expand=True, padx=25, pady=20)
        self.tree = ttk.Treeview(
            table_frame,
            columns=("student", "course", "timestamp"),
            show="headings",
            height=10,
        )
        self.tree.heading("student", text="Student ID / Name")
        self.tree.heading("course", text="Course Code / Name")
        self.tree.heading("timestamp", text="Date and Time")
        self.tree.column("student", width=250)
        self.tree.column("course", width=300)
        self.tree.column("timestamp", width=180)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for rec in self.service.get_all_records():
            self.tree.insert(
                "", "end",
                values=(
                    f"{rec['student_id']} - {rec['student_name']}",
                    f"{rec['course_code']} - {rec['course_name']}",
                    rec["timestamp"],
                ),
            )
