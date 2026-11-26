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
    """Original two-field student registration dialog, connected to the service."""
    window = _dialog(parent, "Register Student", "450x370")
    _title(window, "Register Student", "Enter the student's information.")
    student_id = _field(window, "Student ID", 36)
    name = _field(window, "Full Name", 36)

    def submit():
        try:
            on_submit(student_id.get(), name.get())
            window.destroy()
        except (ValueError, OSError) as exc:
            show_error(window, "Student", exc)

    _buttons(window, submit, "Register Student")
    student_id.focus_set()
    return window


def student_details(parent, student, on_add_completed):
    """Original student details dialog with the completed-course action."""
    window = _dialog(parent, "Student Information", "450x420")
    tk.Label(window, text="Student Information", font=("Arial", 18, "bold"),
             bg=WHITE, fg=BLUE).pack(anchor="w", padx=25, pady=(25, 20))
    for label, value in (("Student ID", student["student_id"]),
                         ("Full Name", student["name"]),
                         ("Completed Courses", ", ".join(sorted(student.get("completed_courses", []))) or "None")):
        tk.Label(window, text=label, font=("Arial", 10, "bold"), bg=WHITE,
                 fg="#333333").pack(anchor="w", padx=25)
        tk.Label(window, text=value, font=("Arial", 11), bg=WHITE,
                 fg="#555555", wraplength=390, justify="left").pack(anchor="w", padx=25, pady=(5, 15))
    buttons = tk.Frame(window, bg=WHITE)
    buttons.pack(fill="x", padx=25, pady=(10, 20))
    tk.Button(buttons, text="Close", command=window.destroy, font=("Arial", 10),
              bg="#E5E7EB", fg="#333333", relief="flat", padx=15, pady=8,
              cursor="hand2").pack(side="right", padx=(10, 0))
    tk.Button(buttons, text="Add Completed Course", command=lambda: _completed_course_dialog(
        window, student["student_id"], on_add_completed), font=("Arial", 10, "bold"),
        bg=BLUE, fg=WHITE, activebackground="#06447D", activeforeground=WHITE,
        relief="flat", padx=15, pady=8, cursor="hand2").pack(side="right")
    return window


def _completed_course_dialog(parent, student_id, on_submit):
    window = _dialog(parent, "Add Completed Course", "400x260")
    _title(window, "Add Completed Course", "Enter the completed course code.")
    course = _field(window, "Course Code", 32)

    def submit():
        try:
            on_submit(student_id, course.get())
            window.destroy()
        except (ValueError, OSError) as exc:
            show_error(window, "Completed Course", exc)

    _buttons(window, submit, "Add Course")


def course_form(parent, courses, on_submit):
    """Original scrollable prerequisite selector and course form."""
    window = _dialog(parent, "Add Course", "450x560")
    _title(window, "Add Course", "Enter the course information.")
    code = _field(window, "Course Code", 36)
    title = _field(window, "Course Name", 36)
    capacity = _field(window, "Course Capacity", 36)
    tk.Label(window, text="Prerequisites", font=("Arial", 10, "bold"),
             bg=WHITE, fg="#333333").pack(anchor="w", padx=25, pady=(0, 5))
    border = tk.Frame(window, bg=WHITE, bd=1, relief="solid")
    border.pack(fill="x", padx=25)
    canvas = tk.Canvas(border, height=105, bg=WHITE, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(border, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    inner = tk.Frame(canvas, bg=WHITE)
    canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")
    inner.bind("<Configure>", lambda _event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(canvas_window, width=event.width))
    no_prerequisites = tk.BooleanVar(value=True)
    selected = {}

    def toggle_none():
        if no_prerequisites.get():
            for variable in selected.values():
                variable.set(False)

    def toggle_course():
        no_prerequisites.set(not any(variable.get() for variable in selected.values()))

    tk.Checkbutton(inner, text="No prerequisites", variable=no_prerequisites,
                   font=("Arial", 10), bg=WHITE, activebackground=WHITE,
                   command=toggle_none).pack(anchor="w", padx=8, pady=5)
    for course_code, details in courses.items():
        variable = tk.BooleanVar(value=False)
        selected[course_code] = variable
        tk.Checkbutton(inner, text=f"{course_code} - {details['name']}", variable=variable,
                       font=("Arial", 10), bg=WHITE, activebackground=WHITE,
                       command=toggle_course).pack(anchor="w", padx=8, pady=3)
    if not courses:
        tk.Label(inner, text="No existing courses available.", font=("Arial", 9),
                 bg=WHITE, fg="#777777").pack(anchor="w", padx=8, pady=3)

    def submit():
        prerequisites = [key for key, variable in selected.items() if variable.get()]
        try:
            on_submit(code.get(), title.get(), capacity.get(), prerequisites)
            window.destroy()
        except (ValueError, OSError) as exc:
            show_error(window, "Course", exc)

    _buttons(window, submit, "Add Course")
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
