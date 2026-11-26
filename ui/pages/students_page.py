
import tkinter as tk
from tkinter import ttk, messagebox

from ui.components.dialogs.student_dialogs import (
    StudentRegistrationDialog,
    ViewStudentDialog,
)


class StudentsPage:

    def __init__(self, parent, student_service, enrollment_service,
                 course_service, on_change=None):
        self.parent = parent
        self.student_service = student_service
        self.enrollment_service = enrollment_service
        self.course_service = course_service
        self.on_change = on_change

        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )

        self.frame.pack(fill="both", expand=True)

        self.create_header()
        self.create_search_bar()
        self.load_students()
        self.create_student_table()
        self.create_bottom_button()

    def create_header(self):

        title = tk.Label(
            self.frame,
            text="Students",
            font=("Arial", 22, "bold"),
            bg="#F1F3F5",
            fg="#07549C"
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        subtitle = tk.Label(
            self.frame,
            text="Manage student records and information",
            font=("Arial", 10),
            bg="#F1F3F5",
            fg="#555555"
        )

        subtitle.pack(
            anchor="w",
            padx=25
        )

    def create_search_bar(self):

        search_frame = tk.Frame(
            self.frame,
            bg="#F1F3F5"
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8,
            padx=(0, 10)
        )

        self.search_entry.insert(
            0,
            "Search by student ID"
        )

        self.search_entry.config(fg="#888888")

        self.search_entry.bind(
            "<FocusIn>",
            self.clear_placeholder
        )

        self.search_entry.bind(
            "<FocusOut>",
            self.restore_placeholder
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_student()
        )

        search_button = tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.search_student
        )

        search_button.pack(side="right")

        self.search_result = tk.Label(
            self.frame,
            text="",
            font=("Arial", 9),
            bg="#F1F3F5",
            fg="#DC3545"
        )

        self.search_result.pack(
            anchor="w",
            padx=25,
            pady=(0, 5)
        )

    def clear_placeholder(self, event=None):

        if self.search_entry.get() == "Search by student ID":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#333333")

    def restore_placeholder(self, event=None):

        if not self.search_entry.get().strip():
            self.search_entry.insert(
                0,
                "Search by student ID"
            )

            self.search_entry.config(fg="#888888")

    def create_student_table(self):

        table_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 10)
        )

        table_title = tk.Label(
            table_frame,
            text="Student Records",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )

        table_title.pack(
            anchor="w",
            padx=15,
            pady=12
        )

        columns = (
            "student_id",
            "name"
        )

        self.student_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        self.student_tree.heading(
            "student_id",
            text="Student ID"
        )

        self.student_tree.heading(
            "name",
            text="Student Name"
        )

        self.student_tree.column(
            "student_id",
            width=150,
            anchor="center"
        )

        self.student_tree.column(
            "name",
            width=250,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_tree.yview
        )

        self.student_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.student_tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=(0, 15)
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=(0, 15)
        )

        self.student_tree.bind(
            "<Double-1>",
            self.open_view_dialog
        )

        self.display_students(self.students)

    def create_bottom_button(self):

        button_frame = tk.Frame(
            self.frame,
            bg="#F1F3F5"
        )

        button_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # Add Student button
        add_button = tk.Button(
            button_frame,
            text="+ Add Student",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.open_registration_dialog
        )

        add_button.pack(side="right")

        # Delete Student button
        delete_button = tk.Button(
            button_frame,
            text="Delete Student",
            font=("Arial", 10, "bold"),
            bg="#DC3545",
            fg="#FFFFFF",
            activebackground="#B02A37",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
            command=self.delete_student
        )

        delete_button.pack(
            side="right",
            padx=(0, 10)
        )

    def display_students(self, students):

        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        for student_id, details in students.items():

            self.student_tree.insert(
                "",
                "end",
                values=(
                    student_id,
                    details["name"]
                )
            )

    def search_student(self):

        student_id = self.search_entry.get().strip()

        if student_id == "Search by student ID" or not student_id:

            self.search_result.config(
                text="Please enter a Student ID.",
                fg="#DC3545"
            )

            self.display_students(self.students)
            return

        student = self.students.get(student_id.upper())

        if student is None:

            self.search_result.config(
                text="Student not found.",
                fg="#DC3545"
            )

            self.display_students({})
            return

        self.search_result.config(
            text="Student found successfully.",
            fg="#16803C"
        )

        self.display_students({
            student_id.upper(): student
        })

    def delete_student(self):

        selected_item = self.student_tree.selection()

        if not selected_item:

            messagebox.showwarning(
                "No Student Selected",
                "Please select a student to delete.",
                parent=self.frame.winfo_toplevel()
            )

            return

        values = self.student_tree.item(
            selected_item[0],
            "values"
        )

        student_id = values[0]
        student_name = values[1]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this student?\n\n"
            f"Student ID: {student_id}\n"
            f"Name: {student_name}",
            parent=self.frame.winfo_toplevel()
        )

        if not confirm:
            return

        try:
            self.enrollment_service.drop_all_for_student(student_id)
            self.student_service.remove(student_id)
        except (ValueError, OSError) as exc:
            messagebox.showerror("Delete Failed", str(exc), parent=self.frame.winfo_toplevel())
            return
        self.load_students()

        #eset search field
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(
            0,
            "Search by student ID"
        )
        self.search_entry.config(fg="#888888")

        # refresh table
        self.display_students(self.students)

        self.search_result.config(
            text="Student deleted successfully.",
            fg="#16803C"
        )
        if self.on_change:
            self.on_change()

    def open_registration_dialog(self):

        StudentRegistrationDialog(self.frame, self._register_student)

    def _register_student(self, student_id, name):
        self.student_service.add(student_id, name)
        self.load_students()
        self.display_students(self.students)
        self.search_result.config(text="Student registered successfully.", fg="#16803C")
        if self.on_change:
            self.on_change()

    def open_view_dialog(self, event=None):

        selected_item = self.student_tree.selection()

        if not selected_item:
            return

        values = self.student_tree.item(
            selected_item[0],
            "values"
        )

        student_id = values[0]

        student = self.students.get(student_id)

        if student is None:
            return

        ViewStudentDialog(
            self.frame.winfo_toplevel(), student_id, student["name"],
            student["completed_courses"], self._add_completed_course,
            self.course_service.all()
        )

    def _add_completed_course(self, student_id, course_code):
        self.student_service.add_completed_course(student_id, course_code)
        self.load_students()
        self.display_students(self.students)
        if self.on_change:
            self.on_change()

    #tempo data 4 UI testing
    def load_students(self):
        """Load the real student records from the student service."""
        self.students = {}
        for s in self.student_service.all():
            self.students[s["student_id"]] = {
                "name": s["name"],
                "completed_courses": set(s.get("completed_courses", [])),
                "email": s.get("email", ""),
            }
