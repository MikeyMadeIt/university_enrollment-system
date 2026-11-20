
import tkinter as tk
from tkinter import ttk

from ui.components.dialogs import (
    AddCourseDialog,
    EnrolledStudentsDialog
)


class CoursesPage:

    def __init__(self, parent):
        self.parent = parent

        # Main page frame
        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )
        self.frame.pack(fill="both", expand=True)

        self.load_placeholder_courses()
        self.load_placeholder_students()

        self.create_header()
        self.create_search_bar()
        self.create_course_table()

    def create_header(self):

        title = tk.Label(
            self.frame,
            text="Courses",
            font=("Arial", 22, "bold"),
            bg="#F1F3F5",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(25, 5))

        subtitle = tk.Label(
            self.frame,
            text="Manage available courses and course information",
            font=("Arial", 10),
            bg="#F1F3F5",
            fg="#555555"
        )
        subtitle.pack(anchor="w", padx=25)

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
            "Search by course code"
        )

        #Course button
        add_button = tk.Button(
            search_frame,
            text="+ Add Course",
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
        add_button.pack(side="right")

    def create_course_table(self):

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

        # Table title
        table_title = tk.Label(
            table_frame,
            text="Available Courses",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        table_title.pack(
            anchor="w",
            padx=15,
            pady=15
        )

        columns = (
            "course_code",
            "course_name",
            "capacity",
            "enrolled"
        )

        self.course_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.course_tree.heading(
            "course_code",
            text="Course Code"
        )

        self.course_tree.heading(
            "course_name",
            text="Course Name"
        )

        self.course_tree.heading(
            "capacity",
            text="Capacity"
        )

        self.course_tree.heading(
            "enrolled",
            text="Enrolled"
        )

        self.course_tree.column(
            "course_code",
            width=130,
            anchor="center"
        )

        self.course_tree.column(
            "course_name",
            width=300,
            anchor="w"
        )

        self.course_tree.column(
            "capacity",
            width=120,
            anchor="center"
        )

        self.course_tree.column(
            "enrolled",
            width=120,
            anchor="center"
        )

        # Insert placeholder course records
        for course_code, details in self.courses.items():

            self.course_tree.insert(
                "",
                "end",
                iid=course_code,
                values=(
                    course_code,
                    details["name"],
                    details["capacity"],
                    len(details["enrolled"])
                )
            )

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.course_tree.yview
        )

        self.course_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.course_tree.pack(
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

        # Double-click event
        self.course_tree.bind(
            "<Double-1>",
            self.open_enrolled_students
        )

    def open_add_course_dialog(self):

        AddCourseDialog(
            self.frame,
            self.courses
        )

    def open_enrolled_students(self, event=None):

        selected_item = self.course_tree.selection()

        if not selected_item:
            return

        course_code = selected_item[0]
        course_details = self.courses[course_code]

        EnrolledStudentsDialog(
            self.frame,
            course_code,
            course_details["name"],
            course_details["enrolled"],
            self.students
        )

    def load_placeholder_courses(self):

        self.courses = {

            "CS101": {
                "name": "Introduction to Computing",
                "capacity": 40,
                "enrolled": {"2026-001", "2026-002"},
                "prerequisites": set()
            },

            "CS102": {
                "name": "Data Structures",
                "capacity": 30,
                "enrolled": set(),
                "prerequisites": {"CS101"}
            },

            "CS103": {
                "name": "Programming 2",
                "capacity": 35,
                "enrolled": set(),
                "prerequisites": {"CS102"}
            },

            "IT101": {
                "name": "Introduction to Information Technology",
                "capacity": 40,
                "enrolled": set(),
                "prerequisites": set()
            },

            "IT102": {
                "name": "Computer Systems and Architecture",
                "capacity": 40,
                "enrolled": set(),
                "prerequisites": {"IT101"}
            }
        }

    def load_placeholder_students(self):

        self.students = {

            "2026-001": {
                "name": "Lopez, Dhan Paul",
                "completed_courses": set()
            },

            "2026-002": {
                "name": "Lopez, Dhan Paul",
                "completed_courses": set()
            }
        }


# Temporary testing
if __name__ == "__main__":

    root = tk.Tk()
    root.title("QCU Enrollment System")
    root.geometry("1000x650")

    CoursesPage(root)

    root.mainloop()
