import tkinter as tk
from tkinter import messagebox, ttk

from algorithms.sorting import bubble_sort
from ui.components.dialogs import confirm, course_form, show_enrolled_students, show_error


BLUE, PAGE, WHITE = "#07549C", "#F1F3F5", "#FFFFFF"


class CoursesPage:
    def __init__(self, parent, course_service, enrollment_service, student_service=None, on_change=None):
        self.parent = parent
        self.courses = course_service
        self.enrollments = enrollment_service
        self.students = student_service
        self.on_change = on_change
        self.frame = tk.Frame(parent, bg=PAGE)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="Courses", font=("Arial", 22, "bold"),
                 bg=PAGE, fg=BLUE).pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame, text="Manage available courses and course information",
                 font=("Arial", 10), bg=PAGE, fg="#555555").pack(anchor="w", padx=25)

        search = tk.Frame(self.frame, bg=PAGE)
        search.pack(fill="x", padx=25, pady=20)
        self.query = tk.StringVar()
        self.search_entry = tk.Entry(search, textvariable=self.query, font=("Arial", 11),
                                     relief="solid", bd=1)
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self._button(search, "Search", self.search, primary=True).pack(side="right")
        self.search_entry.bind("<Return>", lambda _event: self.search())
        self.result = tk.Label(self.frame, text="", font=("Arial", 9), bg=PAGE, fg="#DC3545")
        self.result.pack(anchor="w", padx=25, pady=(0, 5))

        panel = tk.Frame(self.frame, bg=WHITE)
        panel.pack(fill="both", expand=True, padx=25, pady=(0, 10))
        tk.Label(panel, text="Available Courses", font=("Arial", 14, "bold"),
                 bg=WHITE, fg=BLUE).pack(anchor="w", padx=15, pady=12)
        columns = ("course_code", "title", "capacity", "enrollment", "prerequisites")
        self.tree = ttk.Treeview(panel, columns=columns, show="headings", height=12)
        for col, title, width, anchor in (
            ("course_code", "Course Code", 120, "center"), ("title", "Course Name", 250, "w"),
            ("capacity", "Capacity", 100, "center"), ("enrollment", "Enrolled", 110, "center"),
            ("prerequisites", "Prerequisites", 270, "w"),
        ):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor=anchor)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
        self.tree.bind("<Double-1>", self.show_students)

        actions = tk.Frame(self.frame, bg=PAGE)
        actions.pack(fill="x", padx=25, pady=(0, 20))
        self._button(actions, "Sort by capacity", self.sort_capacity).pack(side="left")
        self._button(actions, "Show enrolled students", self.show_students).pack(side="left", padx=10)
        self._button(actions, "Delete Course", self.delete, danger=True).pack(side="right", padx=(0, 10))
        self._button(actions, "+ Add Course", self.open_add_course_dialog, primary=True).pack(side="right")
        self.refresh()

    @staticmethod
    def _button(parent, text, command, primary=False, danger=False):
        bg = "#DC3545" if danger else (BLUE if primary else "#E5E7EB")
        fg = WHITE if primary or danger else "#333333"
        return tk.Button(parent, text=text, command=command, font=("Arial", 10, "bold"),
                         bg=bg, fg=fg, activebackground="#06447D" if primary else bg,
                         activeforeground=WHITE if primary or danger else fg,
                         relief="flat", padx=15, pady=8, cursor="hand2")

    def open_add_course_dialog(self):
        course_form(self.frame, self._add_course)

    def _add_course(self, code, title, capacity, prerequisites):
        self.courses.add(code, title, capacity, prerequisites.split(","))
        self.refresh()
        self.result.config(text="Course added successfully.", fg="#16803C")
        if self.on_change:
            self.on_change()

    def search(self):
        query = self.query.get().strip()
        if not query:
            self.result.config(text="Please enter a course code or keyword.", fg="#DC3545")
            self.refresh()
            return
        rows = self.courses.search(query)
        self._show(rows)
        self.result.config(text=f"{len(rows)} course(s) found." if rows else "No matching courses found.",
                           fg="#16803C" if rows else "#DC3545")

    def sort_capacity(self):
        self._show(bubble_sort(self.courses.all(), "capacity"))

    def show_students(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        code = self.tree.item(selected[0], "values")[0]
        course = self.courses.get(code)
        enrolled = self.enrollments.for_course(code)
        students = [self.students.get(row["student_id"]) if self.students else None for row in enrolled]
        students = [student or {"student_id": row["student_id"], "name": "Unknown"}
                    for row, student in zip(enrolled, students)]
        show_enrolled_students(self.frame, code, course["title"], students)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Course Selected", "Please select a course to delete.", parent=self.frame)
            return
        code = self.tree.item(selected[0], "values")[0]
        if self.courses.has_dependents(code):
            messagebox.showerror("Course", f"{code} is a prerequisite for another course.", parent=self.frame)
            return
        if not confirm(self.frame, "Confirm Deletion", f"Delete course {code} and its active enrollments?"):
            return
        try:
            self.enrollments.drop_all_for_course(code)
            self.courses.remove(code)
            self.refresh()
            if self.on_change:
                self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Delete Failed", exc)

    def refresh(self):
        self._show(self.courses.all())

    def _show(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            count = self.enrollments.count_for_course(row["course_code"])
            self.tree.insert("", "end", values=(row["course_code"], row["title"], row["capacity"],
                                                    f"{count}/{row['capacity']}",
                                                    ", ".join(row.get("prerequisites", []))))
