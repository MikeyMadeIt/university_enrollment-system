
import tkinter as tk
from tkinter import ttk, messagebox


class AddCourseDialog:

    def __init__(self, parent, courses):
        self.parent = parent
        self.courses = courses

        self.window = tk.Toplevel(parent)
        self.window.title("Add Course")
        self.window.geometry("450x560")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.prerequisite_vars = {}
        self.no_prerequisites_var = tk.BooleanVar(value=True)

        self.create_form()

    def create_form(self):

        title = tk.Label(
            self.window,
            text="Add Course",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(20, 5))

        subtitle = tk.Label(
            self.window,
            text="Enter the course information.",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#555555"
        )
        subtitle.pack(anchor="w", padx=25, pady=(0, 15))

        code_label = tk.Label(
            self.window,
            text="Course Code",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        code_label.pack(anchor="w", padx=25)

        self.code_entry = tk.Entry(
            self.window,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        self.code_entry.pack(
            fill="x",
            padx=25,
            pady=(5, 12),
            ipady=6
        )

        name_label = tk.Label(
            self.window,
            text="Course Name",
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
            pady=(5, 12),
            ipady=6
        )

        capacity_label = tk.Label(
            self.window,
            text="Course Capacity",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        capacity_label.pack(anchor="w", padx=25)

        self.capacity_entry = tk.Entry(
            self.window,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        self.capacity_entry.pack(
            fill="x",
            padx=25,
            pady=(5, 12),
            ipady=6
        )

        prerequisite_label = tk.Label(
            self.window,
            text="Prerequisites",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        prerequisite_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 5)
        )

        prerequisite_frame = tk.Frame(
            self.window,
            bg="#FFFFFF",
            bd=1,
            relief="solid"
        )
        prerequisite_frame.pack(
            fill="x",
            padx=25
        )

        self.prerequisite_canvas = tk.Canvas(
            prerequisite_frame,
            height=105,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.prerequisite_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            prerequisite_frame,
            orient="vertical",
            command=self.prerequisite_canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.prerequisite_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.prerequisite_inner_frame = tk.Frame(
            self.prerequisite_canvas,
            bg="#FFFFFF"
        )

        self.canvas_window = self.prerequisite_canvas.create_window(
            (0, 0),
            window=self.prerequisite_inner_frame,
            anchor="nw"
        )

        self.prerequisite_inner_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.prerequisite_canvas.bind(
            "<Configure>",
            self.update_canvas_width
        )

        no_prerequisites_check = tk.Checkbutton(
            self.prerequisite_inner_frame,
            text="No prerequisites",
            variable=self.no_prerequisites_var,
            font=("Arial", 10),
            bg="#FFFFFF",
            activebackground="#FFFFFF",
            command=self.toggle_no_prerequisites
        )
        no_prerequisites_check.pack(
            anchor="w",
            padx=8,
            pady=5
        )

        for course_code, details in self.courses.items():

            prerequisite_var = tk.BooleanVar(value=False)

            self.prerequisite_vars[course_code] = prerequisite_var

            course_name = details["name"]

            checkbutton = tk.Checkbutton(
                self.prerequisite_inner_frame,
                text=f"{course_code} - {course_name}",
                variable=prerequisite_var,
                font=("Arial", 10),
                bg="#FFFFFF",
                activebackground="#FFFFFF",
                command=self.toggle_course_prerequisite
            )
            checkbutton.pack(
                anchor="w",
                padx=8,
                pady=3
            )

        if not self.courses:
            empty_label = tk.Label(
                self.prerequisite_inner_frame,
                text="No existing courses available.",
                font=("Arial", 9),
                bg="#FFFFFF",
                fg="#777777"
            )
            empty_label.pack(anchor="w", padx=8, pady=3)

        button_frame = tk.Frame(
            self.window,
            bg="#FFFFFF"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=(15, 15)
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
            cursor="hand2"
        )
        add_button.pack(side="right")

    def update_scroll_region(self, event=None):
        self.prerequisite_canvas.configure(
            scrollregion=self.prerequisite_canvas.bbox("all")
        )

    def update_canvas_width(self, event):
        self.prerequisite_canvas.itemconfigure(
            self.canvas_window,
            width=event.width
        )

    def toggle_no_prerequisites(self):

        if self.no_prerequisites_var.get():
            for variable in self.prerequisite_vars.values():
                variable.set(False)

    def toggle_course_prerequisite(self):

        selected = any(
            variable.get()
            for variable in self.prerequisite_vars.values()
        )

        if selected:
            self.no_prerequisites_var.set(False)
        else:
            self.no_prerequisites_var.set(True)

    def get_selected_prerequisites(self):

        return {
            course_code
            for course_code, variable in self.prerequisite_vars.items()
            if variable.get()
        }


class EnrolledStudentsDialog:

    def __init__(
        self,
        parent,
        course_code,
        course_name,
        enrolled_ids,
        students
    ):
        self.window = tk.Toplevel(parent)
        self.window.title("Enrolled Students")
        self.window.geometry("650x570")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        self.window.transient(parent)
        self.window.grab_set()

        self.create_form(
            course_code,
            course_name,
            enrolled_ids,
            students
        )

    def create_form(
        self,
        course_code,
        course_name,
        enrolled_ids,
        students
    ):

        title = tk.Label(
            self.window,
            text="Enrolled Students",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(25, 5))

        subtitle = tk.Label(
            self.window,
            text=f"{course_code} - {course_name}",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#555555"
        )
        subtitle.pack(anchor="w", padx=25, pady=(0, 15))

        prerequisite_label = tk.Label(
            self.window,
            text="Course Prerequisites",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        prerequisite_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 5)
        )

        prerequisite_frame = tk.Frame(
            self.window,
            bg="#F8FAFC",
            bd=1,
            relief="solid"
        )
        prerequisite_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        #tempo data 4 testing ui
        placeholder_prerequisites = {
            "CS101": [],
            "CS102": [
                ("CS101", "Introduction to Computing")
            ],
            "CS103": [
                ("CS101", "Introduction to Computing"),
                ("CS102", "Data Structures")
            ],
            "IT101": [],
            "IT102": [
                ("IT101", "Introduction to Information Technology")
            ]
        }

        prerequisites = placeholder_prerequisites.get(
            course_code,
            []
        )

        if prerequisites:

            for prerequisite_code, prerequisite_name in prerequisites:

                prerequisite_item = tk.Label(
                    prerequisite_frame,
                    text=f"• {prerequisite_code} - {prerequisite_name}",
                    font=("Arial", 10),
                    bg="#F8FAFC",
                    fg="#555555"
                )
                prerequisite_item.pack(
                    anchor="w",
                    padx=12,
                    pady=4
                )

        else:

            no_prerequisites_label = tk.Label(
                prerequisite_frame,
                text="No prerequisites",
                font=("Arial", 10),
                bg="#F8FAFC",
                fg="#777777"
            )
            no_prerequisites_label.pack(
                anchor="w",
                padx=12,
                pady=8
            )

        students_label = tk.Label(
            self.window,
            text="Enrolled Students",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        students_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 5)
        )

        table_frame = tk.Frame(
            self.window,
            bg="#FFFFFF"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25
        )

        columns = ("student_id", "student_name")

        self.student_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        self.student_table.heading(
            "student_id",
            text="Student ID"
        )

        self.student_table.heading(
            "student_name",
            text="Student Name"
        )

        self.student_table.column(
            "student_id",
            width=150,
            anchor="center"
        )

        self.student_table.column(
            "student_name",
            width=400,
            anchor="w"
        )

        self.student_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_table.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.student_table.configure(
            yscrollcommand=scrollbar.set
        )

        for student_id in sorted(enrolled_ids):

            student_details = students.get(student_id, {})

            student_name = student_details.get(
                "name",
                "Name unavailable"
            )

            self.student_table.insert(
                "",
                "end",
                values=(student_id, student_name)
            )

        if not enrolled_ids:
            self.student_table.insert(
                "",
                "end",
                values=("", "No students enrolled.")
            )

        button_frame = tk.Frame(
            self.window,
            bg="#FFFFFF"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        drop_button = tk.Button(
            button_frame,
            text="Drop Student",
            font=("Arial", 10, "bold"),
            bg="#DC2626",
            fg="#FFFFFF",
            activebackground="#B91C1C",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.confirm_drop
        )
        drop_button.pack(side="left")

        close_button = tk.Button(
            button_frame,
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
        close_button.pack(side="right")

    def confirm_drop(self):

        selected_item = self.student_table.selection()

        if not selected_item:
            messagebox.showwarning(
                "No Student Selected",
                "Please select a student first.",
                parent=self.window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Drop",
            "Are you sure you want to drop the selected student?",
            parent=self.window
        )
