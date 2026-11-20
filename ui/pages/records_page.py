
import tkinter as tk
from tkinter import ttk


class RecordsPage:

    def __init__(self, parent):
        self.parent = parent

        # Main page frame
        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )
        self.frame.pack(fill="both", expand=True)

        self.load_placeholder_data()

        self.create_header()
        self.create_enrollment_table()
        self.create_student_search()

    def create_header(self):

        title = tk.Label(
            self.frame,
            text="Enrollment Records",
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
            text="View enrollment records and student course schedules",
            font=("Arial", 10),
            bg="#F1F3F5",
            fg="#555555"
        )
        subtitle.pack(
            anchor="w",
            padx=25
        )

    def create_enrollment_table(self):

        # Enrollment records container
        table_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF"
        )
        table_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        # Section title
        section_title = tk.Label(
            table_frame,
            text="All Enrollment Records",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        section_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # Table container
        tree_frame = tk.Frame(
            table_frame,
            bg="#FFFFFF"
        )
        tree_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

        # Table style
        style = ttk.Style()

        style.configure(
            "Reports.Treeview",
            font=("Arial", 10),
            rowheight=35
        )

        style.configure(
            "Reports.Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        # Enrollment records table
        columns = (
            "student",
            "course",
            "timestamp"
        )

        self.enrollment_table = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=4,
            style="Reports.Treeview"
        )

        self.enrollment_table.heading(
            "student",
            text="Student ID / Name"
        )

        self.enrollment_table.heading(
            "course",
            text="Course Code / Name"
        )

        self.enrollment_table.heading(
            "timestamp",
            text="Date and Time"
        )

        self.enrollment_table.column(
            "student",
            width=250,
            minwidth=150,
            anchor="w",
            stretch=True
        )

        self.enrollment_table.column(
            "course",
            width=350,
            minwidth=200,
            anchor="w",
            stretch=True
        )

        self.enrollment_table.column(
            "timestamp",
            width=200,
            minwidth=150,
            anchor="w",
            stretch=True
        )

        # Vertical scrollbar only
        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.enrollment_table.yview
        )

        self.enrollment_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.enrollment_table.pack(
            side="left",
            fill="x",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Insert placeholder records
        for record in self.enrollment_records:

            student_text = (
                f"{record['student_id']} - "
                f"{record['student_name']}"
            )

            course_text = (
                f"{record['course_code']} - "
                f"{record['course_name']}"
            )

            self.enrollment_table.insert(
                "",
                "end",
                values=(
                    student_text,
                    course_text,
                    record["timestamp"]
                )
            )

    def create_student_search(self):

        # Student search container
        search_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF"
        )
        search_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        # Section title
        section_title = tk.Label(
            search_frame,
            text="Student Enrollment Search",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        section_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        # Search input
        input_frame = tk.Frame(
            search_frame,
            bg="#FFFFFF"
        )
        input_frame.pack(
            fill="x",
            padx=15
        )

        self.student_id_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        self.student_id_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8,
            padx=(0, 10)
        )

        search_button = tk.Button(
            input_frame,
            text="Search Student",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.search_student
        )
        search_button.pack(side="right")

        # Search result
        self.search_result = tk.Label(
            search_frame,
            text="",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#DC3545"
        )
        self.search_result.pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        # Student name
        self.student_name_label = tk.Label(
            search_frame,
            text="",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        self.student_name_label.pack(
            anchor="w",
            padx=15,
            pady=(5, 5)
        )

        # Scrollable enrolled courses container
        course_container = tk.Frame(
            search_frame,
            bg="#FFFFFF"
        )
        course_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

        self.course_canvas = tk.Canvas(
            course_container,
            bg="#FFFFFF",
            highlightthickness=0,
            height=130
        )
        self.course_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        course_scrollbar = ttk.Scrollbar(
            course_container,
            orient="vertical",
            command=self.course_canvas.yview
        )
        course_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.course_canvas.configure(
            yscrollcommand=course_scrollbar.set
        )

        self.course_result_frame = tk.Frame(
            self.course_canvas,
            bg="#FFFFFF"
        )

        self.course_canvas_window = self.course_canvas.create_window(
            (0, 0),
            window=self.course_result_frame,
            anchor="nw"
        )

        self.course_result_frame.bind(
            "<Configure>",
            self.update_course_scroll
        )

        self.course_canvas.bind(
            "<Configure>",
            self.update_course_canvas_width
        )

    def update_course_scroll(self, event=None):

        self.course_canvas.configure(
            scrollregion=self.course_canvas.bbox("all")
        )

    def update_course_canvas_width(self, event):

        self.course_canvas.itemconfigure(
            self.course_canvas_window,
            width=event.width
        )

    def search_student(self):

        student_id = self.student_id_entry.get().strip()

        for widget in self.course_result_frame.winfo_children():
            widget.destroy()

        self.student_name_label.config(text="")

        if not student_id:
            self.search_result.config(
                text="Please enter a Student ID.",
                fg="#DC3545"
            )
            return

        #input "x" displays student not found (testing)
        if student_id == "x":
            self.search_result.config(
                text="Student not found.",
                fg="#DC3545"
            )
            return

        # Display placeholder student for any other input
        student_records = self.enrollment_records

        student_name = student_records[0]["student_name"]

        self.search_result.config(
            text="Student records found successfully.",
            fg="#16803C"
        )

        self.student_name_label.config(
            text=f"Student: {student_name}"
        )

        # Display all placeholder enrolled courses
        for record in student_records:
            course_text = (
                f"{record['course_code']} - "
                f"{record['course_name']}"
            )

            course_frame = tk.Frame(
                self.course_result_frame,
                bg="#F1F3F5"
            )
            course_frame.pack(
                fill="x",
                pady=3
            )

            tk.Label(
                course_frame,
                text=course_text,
                font=("Arial", 10, "bold"),
                bg="#F1F3F5",
                fg="#333333"
            ).pack(
                anchor="w",
                padx=10,
                pady=(8, 2)
            )

            tk.Label(
                course_frame,
                text="Schedule: TBA",
                font=("Arial", 9),
                bg="#F1F3F5",
                fg="#555555"
            ).pack(
                anchor="w",
                padx=10,
                pady=(0, 8)
            )

        self.course_canvas.yview_moveto(0)

    #tempo data for ui testing only
    def load_placeholder_data(self):
        self.enrollment_records = [
            {
                "student_id": "2026-001",
                "student_name": "Lopez, Dhan Paul",
                "course_code": "CS101",
                "course_name": "Introduction to Computing",
                "timestamp": "Nov 20, 2026, 10:30 AM",
                "schedule": "TBA"
            },

            {
                "student_id": "2026-001",
                "student_name": "Lopez, Dhan Paul",
                "course_code": "CS101",
                "course_name": "Introduction to Computing",
                "timestamp": "Nov 20, 2026, 10:30 AM",
                "schedule": "TBA"
            },

            {
                "student_id": "2026-001",
                "student_name": "Lopez, Dhan Paul",
                "course_code": "CS101",
                "course_name": "Introduction to Computing",
                "timestamp": "Nov 20, 2026, 10:30 AM",
                "schedule": "TBA"
            },

            {
                "student_id": "2026-001",
                "student_name": "Lopez, Dhan Paul",
                "course_code": "IT101",
                "course_name": "Introduction to Information Technology",
                "timestamp": "Nov 20, 2026, 1:00 PM",
                "schedule": "TBA"
            },
        ]
