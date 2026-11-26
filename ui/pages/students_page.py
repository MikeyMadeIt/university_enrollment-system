import tkinter as tk
from tkinter import messagebox, ttk

from algorithms.sorting import bubble_sort
from ui.components.dialogs import confirm, show_error


class StudentsPage:
    def __init__(self, parent, student_service, enrollment_service, on_change=None):
        self.students, self.enrollments, self.on_change = student_service, enrollment_service, on_change
        self.frame = ttk.Frame(parent, padding=18)
        self.frame.pack(fill="both", expand=True)
        ttk.Label(self.frame, text="Students", font=("Arial", 21, "bold")).pack(anchor="w")
        form = ttk.LabelFrame(self.frame, text="Register student", padding=10)
        form.pack(fill="x", pady=12)
        self.student_id, self.name = tk.StringVar(), tk.StringVar()
        self.email, self.completed = tk.StringVar(), tk.StringVar()
        fields = (("Student ID", self.student_id, 15), ("Name", self.name, 23),
                  ("Email", self.email, 25), ("Completed courses (comma separated)", self.completed, 32))
        for col, (label, var, width) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=0, column=col, sticky="w", padx=4)
            ttk.Entry(form, textvariable=var, width=width).grid(row=1, column=col, padx=4, pady=4)
        ttk.Button(form, text="Add student", command=self.add_student).grid(row=1, column=4, padx=5)

        controls = ttk.Frame(self.frame)
        controls.pack(fill="x", pady=(0, 8))
        self.query = tk.StringVar()
        ttk.Entry(controls, textvariable=self.query).pack(side="left", fill="x", expand=True)
        ttk.Button(controls, text="Search ID/name", command=self.search).pack(side="left", padx=5)
        ttk.Button(controls, text="Sort by name", command=self.sort_by_name).pack(side="left")
        ttk.Button(controls, text="Mark completed course", command=self.mark_completed).pack(side="left", padx=5)
        ttk.Button(controls, text="Delete selected", command=self.delete).pack(side="right")
        cols = ("student_id", "name", "email", "completed_courses")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        for col, width in zip(cols, (130, 220, 220, 300)):
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.refresh()

    def add_student(self):
        try:
            self.students.add(self.student_id.get(), self.name.get(), self.email.get(), self.completed.get().split(","))
            for field in (self.student_id, self.name, self.email, self.completed): field.set("")
            self.refresh()
            if self.on_change: self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Student", exc)

    def search(self):
        result = self.students.search(self.query.get())
        self._show([result] if result else [])

    def sort_by_name(self):
        self._show(bubble_sort(self.students.all(), "name"))

    def mark_completed(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Student", "Select a student first.", parent=self.frame)
            return
        course = self.query.get().strip()
        if not course:
            messagebox.showinfo("Student", "Enter the completed course code in the search field.", parent=self.frame)
            return
        sid = self.tree.item(selected[0], "values")[0]
        try:
            self.students.add_completed_course(sid, course)
            self.refresh()
            if self.on_change: self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Student", exc)

    def delete(self):
        selected = self.tree.selection()
        if not selected: return
        sid = self.tree.item(selected[0], "values")[0]
        if not confirm(self.frame, "Delete student", f"Delete {sid} and all active enrollments?"):
            return
        try:
            self.enrollments.drop_all_for_student(sid)
            self.students.remove(sid)
            self.refresh()
            if self.on_change: self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Student", exc)

    def refresh(self):
        self._show(self.students.all())

    def _show(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=(row["student_id"], row["name"], row.get("email", ""), ", ".join(row.get("completed_courses", []))))
