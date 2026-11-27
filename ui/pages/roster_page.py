import tkinter as tk
from tkinter import ttk
from services.course_service import CourseService
from services.student_service import StudentService


class RosterPage:
    def __init__(self, parent):
        self.parent = parent
        self.course_service = CourseService()
        self.student_service = StudentService()
        self.frame = tk.Frame(parent, bg="#F1F3F5")
        self.frame.pack(fill="both", expand=True)
        self._build()
        self._load_courses()

    def _build(self):
        tk.Label(self.frame, text="Course Roster", font=("Arial", 22, "bold"),
                 bg="#F1F3F5", fg="#07549C").pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame,
                 text="Students enrolled in a particular course",
                 font=("Arial", 10), bg="#F1F3F5", fg="#555555"
                 ).pack(anchor="w", padx=25)

        top = tk.Frame(self.frame, bg="#F1F3F5")
        top.pack(fill="x", padx=25, pady=15)
        tk.Label(top, text="Course:", bg="#F1F3F5").pack(side="left")
        self.course_var = tk.StringVar()
        self.combo = ttk.Combobox(top, textvariable=self.course_var,
                                   state="readonly", width=40)
        self.combo.pack(side="left", padx=10)
        tk.Button(top, text="Show Roster", bg="#07549C", fg="white",
                  relief="flat", padx=15, pady=6, command=self.refresh
                  ).pack(side="left")

        self.info_label = tk.Label(self.frame, text="", font=("Arial", 11),
                                    bg="#F1F3F5", fg="#333")
        self.info_label.pack(anchor="w", padx=25, pady=(0, 10))

        tf = tk.Frame(self.frame, bg="white")
        tf.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        self.tree = ttk.Treeview(tf, columns=("sid", "name"),
                                  show="headings", height=12)
        self.tree.heading("sid", text="Student ID")
        self.tree.heading("name", text="Student Name")
        self.tree.column("sid", width=150, anchor="center")
        self.tree.column("name", width=400, anchor="w")
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True,
                       padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", padx=(0, 10), pady=10)

    def _load_courses(self):
        courses = self.course_service.get_all_courses()
        self.combo["values"] = [f"{c} - {i['name']}"
                                 for c, i in courses.items()]
        if self.combo["values"]:
            self.combo.current(0)
            self.refresh()

    def refresh(self):
        selection = self.course_var.get().strip()
        if not selection:
            return
        code = selection.split(" - ")[0].strip()
        course = self.course_service.get_course(code)
        if not course:
            return
        for i in self.tree.get_children():
            self.tree.delete(i)
        enrolled = self.course_service.get_roster(code)
        for sid in enrolled:
            student = self.student_service.get_student(sid)
            name = student["name"] if student else "(missing)"
            self.tree.insert("", "end", values=(sid, name))
        self.info_label.config(
            text=f"{code}: {len(enrolled)}/{course['capacity']} enrolled")
