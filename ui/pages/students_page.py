import tkinter as tk
from tkinter import messagebox, ttk

from algorithms.sorting import bubble_sort
from ui.components.dialogs import confirm, show_error, student_form


BLUE, PAGE, WHITE = "#07549C", "#F1F3F5", "#FFFFFF"


class StudentsPage:
    def __init__(self, parent, student_service, enrollment_service, on_change=None):
        self.parent = parent
        self.students = student_service
        self.enrollments = enrollment_service
        self.on_change = on_change
        self.frame = tk.Frame(parent, bg=PAGE)
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="Students", font=("Arial", 22, "bold"),
                 bg=PAGE, fg=BLUE).pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame, text="Manage student records and information",
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
        tk.Label(panel, text="Student Records", font=("Arial", 14, "bold"),
                 bg=WHITE, fg=BLUE).pack(anchor="w", padx=15, pady=12)
        columns = ("student_id", "name", "email", "completed_courses")
        self.tree = ttk.Treeview(panel, columns=columns, show="headings", height=12)
        for col, title, width, anchor in (
            ("student_id", "Student ID", 130, "center"), ("name", "Student Name", 210, "w"),
            ("email", "Email", 220, "w"), ("completed_courses", "Completed Courses", 300, "w"),
        ):
            self.tree.heading(col, text=title)
            self.tree.column(col, width=width, anchor=anchor)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
        self.tree.bind("<Double-1>", self.view_student)

        actions = tk.Frame(self.frame, bg=PAGE)
        actions.pack(fill="x", padx=25, pady=(0, 20))
        self._button(actions, "Sort by name", self.sort_by_name).pack(side="left")
        tk.Label(actions, text="Completed course:", font=("Arial", 9), bg=PAGE,
                 fg="#555555").pack(side="left", padx=(14, 5))
        self.completed_code = tk.StringVar()
        tk.Entry(actions, textvariable=self.completed_code, font=("Arial", 10),
                 relief="solid", bd=1, width=14).pack(side="left", ipady=4)
        self._button(actions, "Mark completed", self.mark_completed).pack(side="left", padx=7)
        self._button(actions, "Delete Student", self.delete, danger=True).pack(side="right", padx=(0, 10))
        self._button(actions, "+ Add Student", self.open_registration_dialog, primary=True).pack(side="right")
        self.refresh()

    @staticmethod
    def _button(parent, text, command, primary=False, danger=False):
        bg = "#DC3545" if danger else (BLUE if primary else "#E5E7EB")
        fg = WHITE if primary or danger else "#333333"
        return tk.Button(parent, text=text, command=command, font=("Arial", 10, "bold"),
                         bg=bg, fg=fg, activebackground="#06447D" if primary else bg,
                         activeforeground=WHITE if primary or danger else fg,
                         relief="flat", padx=15, pady=8, cursor="hand2")

    def open_registration_dialog(self):
        student_form(self.frame, self._add_student)

    def _add_student(self, student_id, name, email, completed):
        self.students.add(student_id, name, email, completed.split(","))
        self.refresh()
        self.result.config(text="Student registered successfully.", fg="#16803C")
        if self.on_change:
            self.on_change()

    def search(self):
        query = self.query.get().strip()
        if not query:
            self.result.config(text="Please enter a Student ID or name.", fg="#DC3545")
            self.refresh()
            return
        found = self.students.search(query)
        self._show([found] if found else [])
        self.result.config(text="Student found successfully." if found else "Student not found.",
                           fg="#16803C" if found else "#DC3545")

    def sort_by_name(self):
        self._show(bubble_sort(self.students.all(), "name"))

    def mark_completed(self):
        selected = self.tree.selection()
        code = self.completed_code.get().strip()
        if not selected or not code:
            messagebox.showinfo("Student", "Select a student and enter a course code.", parent=self.frame)
            return
        sid = self.tree.item(selected[0], "values")[0]
        try:
            self.students.add_completed_course(sid, code)
            self.refresh()
            if self.on_change:
                self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Student", exc)

    def delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Student Selected", "Please select a student to delete.", parent=self.frame)
            return
        sid = self.tree.item(selected[0], "values")[0]
        if not confirm(self.frame, "Confirm Deletion", f"Delete student {sid} and their active enrollments?"):
            return
        try:
            self.enrollments.drop_all_for_student(sid)
            self.students.remove(sid)
            self.refresh()
            if self.on_change:
                self.on_change()
        except (ValueError, OSError) as exc:
            show_error(self.frame, "Delete Failed", exc)

    def view_student(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        row = self.students.get(self.tree.item(selected[0], "values")[0])
        if row:
            completed = ", ".join(row.get("completed_courses", [])) or "None"
            messagebox.showinfo("Student Information",
                                f"{row['student_id']} - {row['name']}\nEmail: {row.get('email', '')}\nCompleted courses: {completed}",
                                parent=self.frame)

    def refresh(self):
        self._show(self.students.all())

    def _show(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", "end", values=(row["student_id"], row["name"], row.get("email", ""),
                                                   ", ".join(row.get("completed_courses", []))))
