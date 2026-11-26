"""Modal dialogs styled to match the original QCU interface."""

import tkinter as tk
from tkinter import messagebox, ttk

BLUE = "#07549C"
PAGE = "#F1F3F5"
WHITE = "#FFFFFF"


def show_error(parent, title, error):
    messagebox.showerror(title, str(error), parent=parent)


def confirm(parent, title, message):
    return messagebox.askyesno(title, message, parent=parent)


def student_form(parent, on_submit):
    """Show the original registration form and submit its values to the page."""
    window = _dialog(parent, "Register Student", "430x390")
    _title(window, "Register Student", "Enter the student information.")
    fields = []
    for label, width in (("Student ID", 34), ("Student Name", 34),
                         ("Email Address", 34), ("Completed Courses (comma separated)", 34)):
        fields.append(_field(window, label, width))

    def submit():
        try:
            on_submit(*(entry.get() for entry in fields))
            window.destroy()
        except (ValueError, OSError) as exc:
            show_error(window, "Student", exc)

    _buttons(window, submit, "Register Student")
    window.bind("<Return>", lambda _event: submit())
    fields[0].focus_set()
    return window


def course_form(parent, on_submit):
    """Show a course form matching the original white modal style."""
    window = _dialog(parent, "Add Course", "450x430")
    _title(window, "Add Course", "Enter the course information.")
    code = _field(window, "Course Code", 36)
    title = _field(window, "Course Name", 36)
    capacity = _field(window, "Course Capacity", 36)
    prerequisites = _field(window, "Prerequisites (comma separated)", 36)

    def submit():
        try:
            on_submit(code.get(), title.get(), capacity.get(), prerequisites.get())
            window.destroy()
        except (ValueError, OSError) as exc:
            show_error(window, "Course", exc)

    _buttons(window, submit, "Add Course")
    window.bind("<Return>", lambda _event: submit())
    code.focus_set()
    return window


def show_enrolled_students(parent, course_code, course_title, students):
    window = _dialog(parent, "Enrolled Students", "560x480")
    _title(window, "Enrolled Students", f"{course_code} - {course_title}")
    panel = tk.Frame(window, bg=WHITE)
    panel.pack(fill="both", expand=True, padx=25, pady=(4, 18))
    tree = ttk.Treeview(panel, columns=("student_id", "name"), show="headings", height=12)
    tree.heading("student_id", text="Student ID")
    tree.heading("name", text="Student Name")
    tree.column("student_id", width=150, anchor="center")
    tree.column("name", width=320, anchor="w")
    scrollbar = ttk.Scrollbar(panel, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    for student in students:
        tree.insert("", "end", values=(student["student_id"], student["name"]))
    tk.Button(window, text="Close", command=window.destroy, font=("Arial", 10),
              bg="#E5E7EB", fg="#333333", relief="flat", padx=18, pady=8,
              cursor="hand2").pack(anchor="e", padx=25, pady=(0, 20))
    return window


def _dialog(parent, title, geometry):
    window = tk.Toplevel(parent)
    window.title(title)
    window.geometry(geometry)
    window.configure(bg=WHITE)
    window.resizable(False, False)
    window.transient(parent.winfo_toplevel())
    window.grab_set()
    return window


def _title(window, title, subtitle):
    tk.Label(window, text=title, font=("Arial", 18, "bold"), bg=WHITE,
             fg=BLUE).pack(anchor="w", padx=25, pady=(20, 5))
    tk.Label(window, text=subtitle, font=("Arial", 10), bg=WHITE,
             fg="#555555").pack(anchor="w", padx=25, pady=(0, 15))


def _field(parent, label, width):
    tk.Label(parent, text=label, font=("Arial", 10, "bold"), bg=WHITE,
             fg="#333333").pack(anchor="w", padx=25)
    entry = tk.Entry(parent, font=("Arial", 11), relief="solid", bd=1, width=width)
    entry.pack(fill="x", padx=25, pady=(5, 12), ipady=6)
    return entry


def _buttons(window, submit, label):
    frame = tk.Frame(window, bg=WHITE)
    frame.pack(fill="x", padx=25, pady=(10, 20))
    tk.Button(frame, text="Cancel", command=window.destroy, font=("Arial", 10),
              bg="#E5E7EB", fg="#333333", relief="flat", padx=15, pady=8,
              cursor="hand2").pack(side="right", padx=(10, 0))
    tk.Button(frame, text=label, command=submit, font=("Arial", 10, "bold"),
              bg=BLUE, fg=WHITE, activebackground="#06447D", activeforeground=WHITE,
              relief="flat", padx=15, pady=8, cursor="hand2").pack(side="right")
