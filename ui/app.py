"""Tkinter GUI: Students / Courses / Enrollment tabs."""

import tkinter as tk
from tkinter import ttk, messagebox


class App(tk.Tk):
    def __init__(self, student_service, course_service, enrollment_service):
        super().__init__()
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service

        self.title("University Enrollment System")
        self.geometry("980x640")
        self.minsize(820, 540)

        self.status = tk.StringVar(value="Ready")

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=(8, 0))

        self.students_tab = StudentsTab(notebook, self)
        self.courses_tab = CoursesTab(notebook, self)
        self.enroll_tab = EnrollmentTab(notebook, self)

        notebook.add(self.students_tab, text="Students")
        notebook.add(self.courses_tab, text="Courses")
        notebook.add(self.enroll_tab, text="Enrollment")
        notebook.bind("<<NotebookTabChanged>>", lambda e: self._refresh_active(notebook))

        ttk.Label(self, textvariable=self.status, anchor="w",
                  relief="sunken", padding=4).pack(fill="x", side="bottom")

        self.refresh_all()

    def set_status(self, msg):
        self.status.set(msg)

    def refresh_all(self):
        self.students_tab.refresh()
        self.courses_tab.refresh()
        self.enroll_tab.refresh()

    def _refresh_active(self, notebook):
        tabs = (self.students_tab, self.courses_tab, self.enroll_tab)
        idx = notebook.index(notebook.select())
        tabs[idx].refresh()


class StudentsTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=10)
        self.app = app
        self._build()

    def _build(self):
        form = ttk.LabelFrame(self, text="Add Student", padding=8)
        form.pack(fill="x", pady=(0, 8))

        ttk.Label(form, text="ID:").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.id_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.id_var, width=14).grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text="Name:").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var, width=22).grid(row=0, column=3, padx=4, pady=4)

        ttk.Label(form, text="Email:").grid(row=0, column=4, sticky="e", padx=4, pady=4)
        self.email_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.email_var, width=24).grid(row=0, column=5, padx=4, pady=4)

        ttk.Label(form, text="Completed (comma-separated):").grid(
            row=1, column=0, sticky="e", padx=4, pady=4)
        self.completed_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.completed_var, width=42).grid(
            row=1, column=1, columnspan=5, sticky="we", padx=4, pady=4)

        ttk.Button(form, text="Add Student", command=self.add_student).grid(
            row=0, column=6, padx=4, pady=4)
        ttk.Button(form, text="Delete Selected", command=self.delete_selected).grid(
            row=1, column=6, padx=4, pady=4)

        cols = ("student_id", "name", "email", "completed")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (100, 200, 240, 260)):
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for s in self.app.student_service.all():
            self.tree.insert("", "end", values=(
                s["student_id"], s["name"], s["email"],
                ", ".join(s.get("completed_courses", []))))

    def add_student(self):
        try:
            self.app.student_service.add(
                self.id_var.get(), self.name_var.get(),
                self.email_var.get(), self.completed_var.get().split(","))
            for v in (self.id_var, self.name_var, self.email_var, self.completed_var):
                v.set("")
            self.app.set_status("Student added.")
            self.app.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        sid = self.tree.item(sel[0], "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete student {sid} and their enrollments?"):
            return
        try:
            self.app.enrollment_service.drop_all_for_student(sid)
            self.app.student_service.remove(sid)
            self.app.set_status(f"Student {sid} deleted.")
            self.app.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class CoursesTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=10)
        self.app = app
        self._build()

    def _build(self):
        form = ttk.LabelFrame(self, text="Add Course", padding=8)
        form.pack(fill="x", pady=(0, 8))

        ttk.Label(form, text="Code:").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.code_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.code_var, width=14).grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text="Title:").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.title_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.title_var, width=28).grid(row=0, column=3, padx=4, pady=4)

        ttk.Label(form, text="Capacity:").grid(row=0, column=4, sticky="e", padx=4, pady=4)
        self.cap_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.cap_var, width=8).grid(row=0, column=5, padx=4, pady=4)

        ttk.Label(form, text="Prerequisites (comma-separated):").grid(
            row=1, column=0, sticky="e", padx=4, pady=4)
        self.prereq_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.prereq_var, width=42).grid(
            row=1, column=1, columnspan=5, sticky="we", padx=4, pady=4)

        ttk.Button(form, text="Add Course", command=self.add_course).grid(
            row=0, column=6, padx=4, pady=4)
        ttk.Button(form, text="Delete Selected", command=self.delete_selected).grid(
            row=1, column=6, padx=4, pady=4)

        cols = ("course_code", "title", "capacity", "prerequisites", "enrolled")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (110, 240, 90, 260, 90)):
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for c in self.app.course_service.all():
            enrolled = self.app.enrollment_service.count_for_course(c["course_code"])
            self.tree.insert("", "end", values=(
                c["course_code"], c["title"], c["capacity"],
                ", ".join(c.get("prerequisites", [])),
                f'{enrolled}/{c["capacity"]}'))

    def add_course(self):
        try:
            self.app.course_service.add(
                self.code_var.get(), self.title_var.get(),
                self.cap_var.get(), self.prereq_var.get().split(","))
            for v in (self.code_var, self.title_var, self.cap_var, self.prereq_var):
                v.set("")
            self.app.set_status("Course added.")
            self.app.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        code = self.tree.item(sel[0], "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete course {code} and its enrollments?"):
            return
        try:
            self.app.enrollment_service.drop_all_for_course(code)
            self.app.course_service.remove(code)
            self.app.set_status(f"Course {code} deleted.")
            self.app.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class EnrollmentTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, padding=10)
        self.app = app
        self._build()

    def _build(self):
        form = ttk.LabelFrame(self, text="Enroll / Drop", padding=8)
        form.pack(fill="x", pady=(0, 8))

        ttk.Label(form, text="Student:").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        self.student_var = tk.StringVar()
        self.student_combo = ttk.Combobox(
            form, textvariable=self.student_var, state="readonly", width=30)
        self.student_combo.grid(row=0, column=1, padx=4, pady=4)

        ttk.Label(form, text="Course:").grid(row=0, column=2, sticky="e", padx=4, pady=4)
        self.course_var = tk.StringVar()
        self.course_combo = ttk.Combobox(
            form, textvariable=self.course_var, state="readonly", width=46)
        self.course_combo.grid(row=0, column=3, padx=4, pady=4)

        ttk.Button(form, text="Enroll", command=self.enroll).grid(
            row=0, column=4, padx=4, pady=4)
        ttk.Button(form, text="Drop Selected", command=self.drop_selected).grid(
            row=0, column=5, padx=4, pady=4)

        cols = ("student_id", "student_name", "course_code", "course_title")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=16)
        for c, w in zip(cols, (100, 220, 120, 300)):
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True)

    def refresh(self):
        students = self.app.student_service.all()
        courses = self.app.course_service.all()

        self.student_combo["values"] = [
            f'{s["student_id"]} - {s["name"]}' for s in students
        ]
        self.course_combo["values"] = [
            f'{c["course_code"]} - {c["title"]} '
            f'({self.app.enrollment_service.count_for_course(c["course_code"])}/{c["capacity"]})'
            for c in courses
        ]

        for item in self.tree.get_children():
            self.tree.delete(item)
        for e in self.app.enrollment_service.all():
            s = self.app.student_service.get(e["student_id"]) or {}
            c = self.app.course_service.get(e["course_code"]) or {}
            self.tree.insert("", "end", values=(
                e["student_id"], s.get("name", "?"),
                e["course_code"], c.get("title", "?")))

    def _selected_ids(self):
        sv = self.student_var.get()
        cv = self.course_var.get()
        if not sv or not cv:
            raise ValueError("Select a student and a course first")
        return sv.split(" - ")[0].strip(), cv.split(" - ")[0].strip()

    def enroll(self):
        try:
            sid, code = self._selected_ids()
            self.app.enrollment_service.enroll(sid, code)
            self.app.set_status(f"Enrolled {sid} in {code}.")
            self.app.refresh_all()
        except Exception as e:
            messagebox.showerror("Enrollment failed", str(e))

    def drop_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        sid, code = vals[0], vals[2]
        if not messagebox.askyesno("Confirm", f"Drop {sid} from {code}?"):
            return
        try:
            self.app.enrollment_service.drop(sid, code)
            self.app.set_status(f"Dropped {sid} from {code}.")
            self.app.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))