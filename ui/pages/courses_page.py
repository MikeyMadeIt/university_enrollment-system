import tkinter as tk
from tkinter import messagebox, ttk

from algorithms.sorting import bubble_sort
from ui.components.dialogs import confirm, show_error


class CoursesPage:
    def __init__(self, parent, course_service, enrollment_service, on_change=None):
        self.courses, self.enrollments, self.on_change = course_service, enrollment_service, on_change
        self.frame = ttk.Frame(parent, padding=18)
        self.frame.pack(fill="both", expand=True)
        ttk.Label(self.frame, text="Courses", font=("Arial", 21, "bold")).pack(anchor="w")
        form = ttk.LabelFrame(self.frame, text="Add course", padding=10)
        form.pack(fill="x", pady=12)
        self.code, self.title, self.capacity, self.prereqs = (tk.StringVar() for _ in range(4))
        for col, (label, var, width) in enumerate((("Code", self.code, 14), ("Title", self.title, 23),
                                                   ("Capacity", self.capacity, 10),
                                                   ("Prerequisites (comma separated)", self.prereqs, 34))):
            ttk.Label(form, text=label).grid(row=0, column=col, sticky="w", padx=4)
            ttk.Entry(form, textvariable=var, width=width).grid(row=1, column=col, padx=4, pady=4)
        ttk.Button(form, text="Add course", command=self.add_course).grid(row=1, column=4, padx=5)
        actions = ttk.Frame(self.frame)
        actions.pack(fill="x", pady=(0, 8))
        self.query = tk.StringVar()
        ttk.Entry(actions, textvariable=self.query).pack(side="left", fill="x", expand=True)
        ttk.Button(actions, text="Search", command=self.search).pack(side="left", padx=5)
        ttk.Button(actions, text="Sort by capacity", command=self.sort_capacity).pack(side="left")
        ttk.Button(actions, text="Show enrolled students", command=self.show_students).pack(side="left", padx=5)
        ttk.Button(actions, text="Delete selected", command=self.delete).pack(side="right")
        cols = ("course_code", "title", "capacity", "enrollment", "prerequisites")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings")
        for col, width in zip(cols, (120, 230, 90, 100, 290)):
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.refresh()

    def add_course(self):
        try:
            self.courses.add(self.code.get(), self.title.get(), self.capacity.get(), self.prereqs.get().split(","))
            for value in (self.code, self.title, self.capacity, self.prereqs): value.set("")
            self.refresh()
            if self.on_change: self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Course", exc)

    def search(self):
        self._show(self.courses.search(self.query.get()))

    def sort_capacity(self):
        self._show(bubble_sort(self.courses.all(), "capacity"))

    def show_students(self):
        selected = self.tree.selection()
        if not selected: return
        code = self.tree.item(selected[0], "values")[0]
        ids = [row["student_id"] for row in self.enrollments.for_course(code)]
        messagebox.showinfo(f"Students enrolled in {code}", "\n".join(ids) if ids else "No students enrolled.", parent=self.frame)

    def delete(self):
        selected = self.tree.selection()
        if not selected: return
        code = self.tree.item(selected[0], "values")[0]
        if self.courses.has_dependents(code):
            messagebox.showerror("Course", f"{code} is a prerequisite for another course.", parent=self.frame)
            return
        if not confirm(self.frame, "Delete course", f"Delete {code} and its active enrollments?"):
            return
        try:
            self.enrollments.drop_all_for_course(code)
            self.courses.remove(code)
            self.refresh()
            if self.on_change: self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Course", exc)

    def refresh(self):
        self._show(self.courses.all())

    def _show(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            count = self.enrollments.count_for_course(row["course_code"])
            self.tree.insert("", "end", values=(row["course_code"], row["title"], row["capacity"], f"{count}/{row['capacity']}", ", ".join(row["prerequisites"])))
