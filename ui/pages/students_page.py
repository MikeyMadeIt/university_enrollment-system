import tkinter as tk
from tkinter import ttk
from ui.components.dialogs import StudentRegistrationDialog


class StudentsPage:

    def __init__(self, parent):
        self.parent = parent

        # Main page frame
        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )
        self.frame.pack(fill="both", expand=True)

        self.create_header()
        self.create_search_bar()
        self.load_placeholder_students()
        self.create_student_table()

    def create_header(self):
        # Page title
        title = tk.Label(
            self.frame,
            text="Students",
            font=("Arial", 22, "bold"),
            bg="#F1F3F5",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(25, 5))

        # Page description
        subtitle = tk.Label(
            self.frame,
            text="Manage student records and information",
            font=("Arial", 10),
            bg="#F1F3F5",
            fg="#555555"
        )
        subtitle.pack(anchor="w", padx=25)

    def create_search_bar(self):
        #for search bar and button
        search_frame = tk.Frame(
            self.frame,
            bg="#F1F3F5"
        )
        search_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Search input
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

        # Add Student button
        add_button = tk.Button(
            search_frame,
            text="+ Add Student",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.open_registration_dialog
        )
        add_button.pack(side="right")

    def create_student_table(self):
        # Table container
        table_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        #title
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
            pady=15
        )

        #columns
        columns = (
            "student_id",
            "name",
            "completed_courses"
        )

        self.student_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        #sColumn headings
        self.student_tree.heading(
            "student_id",
            text="Student ID"
        )
        self.student_tree.heading(
            "name",
            text="Student Name"
        )
        self.student_tree.heading(
            "completed_courses",
            text="Completed Courses"
        )

        # Column widths
        self.student_tree.column(
            "student_id",
            width=120,
            anchor="center"
        )
        self.student_tree.column(
            "name",
            width=200,
            anchor="center"
        )
        self.student_tree.column(
            "completed_courses",
            width=250,
            anchor = "center"
        )

        # Display student records
        for student_id, details in self.students.items():
            completed = details["completed_courses"]

            completed_text = ", ".join(sorted(completed)) if completed else "None"

            self.student_tree.insert(
                "",
                "end",
                values=(
                    student_id,
                    details["name"],
                    completed_text
                )
            )

        self.student_tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=(0, 15)
        )

        #scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.student_tree.yview
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=(0, 15)
        )

        self.student_tree.configure(
            yscrollcommand=scrollbar.set
        )

    def open_registration_dialog(self):
        StudentRegistrationDialog(self.frame.winfo_toplevel())

    #placeholder data
    def load_placeholder_students(self):
        self.students = {
            "2026-001": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101"}
            },
            "2026-002": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },
            "2026-003": {
                "name": "Lopez Dhan Paul",
                "completed_courses": set()
            },
            "2026-004": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },
            "2026-005": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-006": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-007": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-008": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-009": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-010": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-011": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-012": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-013": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-014": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-015": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-016": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-017": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-018": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-019": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-020": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-021": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-022": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-023": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-024": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-025": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },"2026-026": {
                "name": "Lopez Dhan Paul",
                "completed_courses": {"CS101", "CS102"}
            },


        }

