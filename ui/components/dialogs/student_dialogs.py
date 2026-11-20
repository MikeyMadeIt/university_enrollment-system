
import tkinter as tk
from tkinter import ttk, messagebox


class StudentRegistrationDialog:

    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Register Student")
        self.window.geometry("450x370")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.create_form()

    def create_form(self):

        title = tk.Label(
            self.window,
            text="Register Student",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(25, 5))

        subtitle = tk.Label(
            self.window,
            text="Enter the student's information.",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#555555"
        )
        subtitle.pack(anchor="w", padx=25, pady=(0, 20))

        id_label = tk.Label(
            self.window,
            text="Student ID",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        id_label.pack(anchor="w", padx=25)

        self.id_entry = tk.Entry(
            self.window,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        self.id_entry.pack(
            fill="x",
            padx=25,
            pady=(5, 15),
            ipady=7
        )

        name_label = tk.Label(
            self.window,
            text="Full Name",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        name_label.pack(anchor="w", padx=25)

        self.name_entry = tk.Entry(
            self.window,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        self.name_entry.pack(
            fill="x",
            padx=25,
            pady=(5, 20),
            ipady=7
        )

        button_frame = tk.Frame(
            self.window,
            bg="#FFFFFF"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 10),
            bg="#E5E7EB",
            fg="#333333",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.window.destroy
        )
        cancel_button.pack(side="right", padx=(10, 0))

        register_button = tk.Button(
            button_frame,
            text="Register Student",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        register_button.pack(side="right")


class ViewStudentDialog:

    def __init__(self, parent, student_id, student_name, completed_courses):

        self.window = tk.Toplevel(parent)
        self.window.title("Student Information")
        self.window.geometry("450x420")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.create_form(
            student_id,
            student_name,
            completed_courses
        )

    def create_form(self, student_id, student_name, completed_courses):

        title = tk.Label(
            self.window,
            text="Student Information",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 20)
        )

        id_label = tk.Label(
            self.window,
            text="Student ID",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )

        id_label.pack(anchor="w", padx=25)

        id_value = tk.Label(
            self.window,
            text=student_id,
            font=("Arial", 11),
            bg="#FFFFFF",
            fg="#555555"
        )

        id_value.pack(
            anchor="w",
            padx=25,
            pady=(5, 15)
        )

        name_label = tk.Label(
            self.window,
            text="Full Name",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )

        name_label.pack(anchor="w", padx=25)

        name_value = tk.Label(
            self.window,
            text=student_name,
            font=("Arial", 11),
            bg="#FFFFFF",
            fg="#555555"
        )

        name_value.pack(
            anchor="w",
            padx=25,
            pady=(5, 15)
        )

        courses_label = tk.Label(
            self.window,
            text="Completed Courses",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )

        courses_label.pack(
            anchor="w",
            padx=25
        )

        courses_text = (
            ", ".join(sorted(completed_courses))
            if completed_courses else "None"
        )

        courses_value = tk.Label(
            self.window,
            text=courses_text,
            font=("Arial", 11),
            bg="#FFFFFF",
            fg="#555555",
            wraplength=390,
            justify="left"
        )

        courses_value.pack(
            anchor="w",
            padx=25,
            pady=(5, 15)
        )

        add_course_button = tk.Button(
            self.window,
            text="+ Add Completed Course",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.open_add_course_dialog
        )

        add_course_button.pack(
            anchor="w",
            padx=25,
            pady=(0, 15)
        )

        close_button = tk.Button(
            self.window,
            text="Close",
            font=("Arial", 10),
            bg="#E5E7EB",
            fg="#333333",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.window.destroy
        )

        close_button.pack(
            anchor="e",
            padx=25,
            pady=(0, 20)
        )

    def open_add_course_dialog(self):

        AddCompletedCourseDialog(self.window)


class AddCompletedCourseDialog:

    def __init__(self, parent):

        self.window = tk.Toplevel(parent)
        self.window.title("Add Completed Course")
        self.window.geometry("400x260")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.create_form()

    def create_form(self):

        title = tk.Label(
            self.window,
            text="Add Completed Course",
            font=("Arial", 17, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(25, 5)
        )

        subtitle = tk.Label(
            self.window,
            text="Select a course to add to the student's records.",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#555555"
        )

        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        course_label = tk.Label(
            self.window,
            text="Course",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )

        course_label.pack(
            anchor="w",
            padx=25
        )

        self.course_combo = ttk.Combobox(
            self.window,
            font=("Arial", 10),
            state="readonly",
            values=[
                "CS101 - Introduction to Computing",
                "CS102 - Data Structures",
                "CS201 - Object-Oriented Programming",
                "CS202 - Computer Organization",
                "CS301 - Database Management",
                "IT101 - Introduction to Information Technology"
            ]
        )

        self.course_combo.pack(
            fill="x",
            padx=25,
            pady=(5, 20),
            ipady=5
        )

        button_frame = tk.Frame(
            self.window,
            bg="#FFFFFF"
        )

        button_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Arial", 10),
            bg="#E5E7EB",
            fg="#333333",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.window.destroy
        )

        cancel_button.pack(
            side="right",
            padx=(10, 0)
        )

        add_button = tk.Button(
            button_frame,
            text="Add Course",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.add_course
        )

        add_button.pack(side="right")

    def add_course(self):

        selected_course = self.course_combo.get()

        if not selected_course:

            messagebox.showwarning(
                "No Course Selected",
                "Please select a course first.",
                parent=self.window
            )

            return

        messagebox.showinfo(
            "jSON",
            "sonion",
            parent=self.window
        )

        self.window.destroy()
