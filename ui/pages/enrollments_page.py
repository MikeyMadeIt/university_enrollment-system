import tkinter as tk
from tkinter import ttk

from ui.components.dialogs import confirm, show_error


BLUE, PAGE, WHITE = "#07549C", "#F1F3F5", "#FFFFFF"


class EnrollmentsPage:
    def __init__(self, parent, student_service, course_service, enrollment_service, on_change=None):
        self.students, self.courses, self.enrollments = student_service, course_service, enrollment_service
        self.on_change = on_change
        self.frame = tk.Frame(parent, bg=PAGE)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="Student Enrollment", font=("Arial", 22, "bold"),
                 bg=PAGE, fg=BLUE).pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame, text="Select a student and an available course to enroll",
                 font=("Arial", 10), bg=PAGE, fg="#555555").pack(anchor="w", padx=25)

        student_panel = tk.Frame(self.frame, bg=WHITE, highlightbackground="#D9DDE2", highlightthickness=1)
        student_panel.pack(fill="x", padx=25, pady=16)
        tk.Label(student_panel, text="Student Information", font=("Arial", 14, "bold"),
                 bg=WHITE, fg=BLUE).pack(anchor="w", padx=15, pady=(12, 8))
        row = tk.Frame(student_panel, bg=WHITE)
        row.pack(fill="x", padx=15, pady=(0, 8))
        tk.Label(row, text="Student ID", font=("Arial", 10, "bold"), bg=WHITE,
                 fg="#333333").pack(side="left", padx=(0, 10))
        self.student_id = tk.StringVar()
        self.student_box = ttk.Combobox(row, textvariable=self.student_id, state="readonly", width=25)
        self.student_box.pack(side="left", ipady=3)
        self._button(row, "Check Student", self.check_student, primary=True).pack(side="left", padx=10)
        self.student_result = tk.Label(student_panel, text="", font=("Arial", 10), bg=WHITE,
                                       fg="#16803C")
        self.student_result.pack(anchor="w", padx=15, pady=(0, 2))
        self.student_name = tk.Label(student_panel, text="", font=("Arial", 11, "bold"),
                                     bg=WHITE, fg="#333333")
        self.student_name.pack(anchor="w", padx=15, pady=(0, 12))

        course_panel = tk.Frame(self.frame, bg=WHITE, highlightbackground="#D9DDE2", highlightthickness=1)
        course_panel.pack(fill="both", expand=True, padx=25, pady=(0, 12))
        tk.Label(course_panel, text="Select Course", font=("Arial", 14, "bold"),
                 bg=WHITE, fg=BLUE).pack(anchor="w", padx=15, pady=(12, 3))
        tk.Label(course_panel, text="Available courses and current capacity",
                 font=("Arial", 9), bg=WHITE, fg="#555555").pack(anchor="w", padx=15, pady=(0, 8))
        list_container = tk.Frame(course_panel, bg=WHITE)
        list_container.pack(fill="both", expand=True, padx=15, pady=(0, 12))
        self.course_canvas = tk.Canvas(list_container, bg=WHITE, height=150, highlightthickness=0)
        self.course_canvas.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.course_canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.course_canvas.configure(yscrollcommand=scrollbar.set)
        self.course_list = tk.Frame(self.course_canvas, bg=WHITE)
        self.course_window = self.course_canvas.create_window((0, 0), window=self.course_list, anchor="nw")
        self.course_list.bind("<Configure>", self.update_course_scroll)
        self.course_canvas.bind("<Configure>", self.update_course_canvas_width)
        self.selected_course = tk.StringVar()

        actions = tk.Frame(self.frame, bg=PAGE)
        actions.pack(fill="x", padx=25, pady=(0, 10))
        self.enrollment_result = tk.Label(actions, text="", font=("Arial", 10, "bold"),
                                          bg=PAGE, fg="#16803C")
        self.enrollment_result.pack(side="left")
        self._button(actions, "Drop Selected", self.drop, danger=True).pack(side="right", padx=(0, 10))
        self._button(actions, "Submit Enrollment", self.enroll, primary=True).pack(side="right")

        records = tk.Frame(self.frame, bg=WHITE, highlightbackground="#D9DDE2", highlightthickness=1)
        records.pack(fill="both", expand=True, padx=25, pady=(0, 18))
        tk.Label(records, text="Current Enrollments", font=("Arial", 12, "bold"),
                 bg=WHITE, fg=BLUE).pack(anchor="w", padx=12, pady=(8, 4))
        columns = ("student_id", "student_name", "course_code", "course_title", "timestamp")
        self.tree = ttk.Treeview(records, columns=columns, show="headings", height=4)
        for col, title, width in (("student_id", "Student ID", 120), ("student_name", "Student Name", 180),
                                  ("course_code", "Course Code", 120), ("course_title", "Course Name", 210),
                                  ("timestamp", "Enrolled", 175)):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=12, pady=(0, 8))
        self.refresh()

    @staticmethod
    def _button(parent, text, command, primary=False, danger=False):
        bg = "#DC3545" if danger else (BLUE if primary else "#E5E7EB")
        fg = "#FFFFFF" if primary or danger else "#333333"
        return tk.Button(parent, text=text, command=command, font=("Arial", 10, "bold"),
                         bg=bg, fg=fg, activebackground="#06447D" if primary else bg,
                         activeforeground=fg, relief="flat", padx=15, pady=8, cursor="hand2")

    def update_course_scroll(self, _event=None):
        self.course_canvas.configure(scrollregion=self.course_canvas.bbox("all"))

    def update_course_canvas_width(self, event):
        self.course_canvas.itemconfigure(self.course_window, width=event.width)

    def check_student(self):
        student = self.students.get(self.student_id.get()) if self.student_id.get() else None
        if student is None:
            self.student_result.config(text="Student ID does not exist.", fg="#DC3545")
            self.student_name.config(text="")
            return
        self.student_result.config(text="Student found successfully.", fg="#16803C")
        self.student_name.config(text=f"Student Name: {student['name']}")

    def enroll(self):
        try:
            self.enrollments.enroll(self.student_id.get(), self.selected_course.get())
            self.enrollment_result.config(text="Enrollment submitted successfully!", fg="#16803C")
            self.refresh()
            if self.on_change:
                self.on_change()
        except (ValueError, OSError) as exc:
            self.enrollment_result.config(text="", fg="#DC3545")
            show_error(self.frame, "Enrollment Failed", exc)

    def drop(self):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        sid, code = values[0], values[2]
        if not confirm(self.frame, "Confirm Drop", f"Drop {sid} from {code}?"):
            return
        try:
            self.enrollments.drop(sid, code)
            self.refresh()
            if self.on_change:
                self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Enrollment", exc)

    def refresh(self):
        students = self.students.all()
        courses = self.courses.all()
        self.student_box["values"] = [row["student_id"] for row in students]
        self.course_canvas.delete("all")
        self.course_list.destroy()
        self.course_list = tk.Frame(self.course_canvas, bg=WHITE)
        self.course_window = self.course_canvas.create_window((0, 0), window=self.course_list, anchor="nw")
        self.course_list.bind("<Configure>", self.update_course_scroll)
        self.course_canvas.configure(scrollregion=self.course_canvas.bbox("all"))
        for course in courses:
            code = course["course_code"]
            count = self.enrollments.count_for_course(code)
            label = f"{code} - {course['title']} ({count}/{course['capacity']})"
            tk.Radiobutton(self.course_list, text=label, variable=self.selected_course, value=code,
                           font=("Arial", 10), bg=WHITE, fg="#333333", activebackground=WHITE,
                           activeforeground=BLUE, selectcolor=WHITE, anchor="w", padx=5, pady=5).pack(fill="x")
        student_names = {row["student_id"]: row["name"] for row in students}
        course_names = {row["course_code"]: row["title"] for row in courses}
        self.tree.delete(*self.tree.get_children())
        for row in self.enrollments.all():
            self.tree.insert("", "end", values=(row["student_id"], student_names.get(row["student_id"], "Unknown"),
                                                   row["course_code"], course_names.get(row["course_code"], "Unknown"),
                                                   row.get("timestamp") or ""))
