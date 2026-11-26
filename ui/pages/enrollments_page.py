import tkinter as tk
from tkinter import messagebox, ttk

from ui.components.dialogs import confirm, show_error


class EnrollmentsPage:
    def __init__(self, parent, student_service, course_service, enrollment_service, on_change=None):
        self.students, self.courses = student_service, course_service
        self.enrollments, self.on_change = enrollment_service, on_change
        self.frame = ttk.Frame(parent, padding=18)
        self.frame.pack(fill="both", expand=True)
        ttk.Label(self.frame, text="Student Enrollment", font=("Arial", 21, "bold")).pack(anchor="w")
        form = ttk.LabelFrame(self.frame, text="Enroll", padding=10)
        form.pack(fill="x", pady=12)
        ttk.Label(form, text="Student ID").grid(row=0, column=0, sticky="w", padx=4)
        ttk.Label(form, text="Course code").grid(row=0, column=1, sticky="w", padx=4)
        self.student_id, self.course_code = tk.StringVar(), tk.StringVar()
        self.student_box = ttk.Combobox(form, textvariable=self.student_id, state="readonly", width=24)
        self.course_box = ttk.Combobox(form, textvariable=self.course_code, state="readonly", width=30)
        self.student_box.grid(row=1, column=0, padx=4, pady=4)
        self.course_box.grid(row=1, column=1, padx=4, pady=4)
        ttk.Button(form, text="Enroll", command=self.enroll).grid(row=1, column=2, padx=8)
        ttk.Button(form, text="Drop selected", command=self.drop).grid(row=1, column=3, padx=4)
        cols = ("student_id", "student_name", "course_code", "course_title", "timestamp")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        for col, width in zip(cols, (120, 190, 120, 220, 190)):
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.refresh()

    def enroll(self):
        try:
            self.enrollments.enroll(self.student_id.get(), self.course_code.get())
            self.refresh()
            if self.on_change: self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Enrollment", exc)

    def drop(self):
        selected = self.tree.selection()
        if not selected: return
        sid, _, code = self.tree.item(selected[0], "values")[:3]
        if not confirm(self.frame, "Drop enrollment", f"Drop {sid} from {code}?"):
            return
        try:
            self.enrollments.drop(sid, code)
            self.refresh()
            if self.on_change: self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Enrollment", exc)

    def refresh(self):
        students = self.students.all()
        courses = self.courses.all()
        self.student_box["values"] = [row["student_id"] for row in students]
        self.course_box["values"] = [row["course_code"] for row in courses]
        student_names = {row["student_id"]: row["name"] for row in students}
        course_names = {row["course_code"]: row["title"] for row in courses}
        self.tree.delete(*self.tree.get_children())
        for row in self.enrollments.all():
            self.tree.insert("", "end", values=(row["student_id"], student_names.get(row["student_id"], "Unknown"),
                                                  row["course_code"], course_names.get(row["course_code"], "Unknown"),
                                                  row.get("timestamp") or ""))
