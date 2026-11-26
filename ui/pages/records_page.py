
import tkinter as tk
from tkinter import messagebox, ttk


class RecordsPage:

    def __init__(self, parent, enrollment_service, student_service, course_service,
                 on_change=None):
        self.parent = parent
        self.enrollment_service = enrollment_service
        self.student_service = student_service
        self.course_service = course_service
        self.on_change = on_change

        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )
        self.frame.pack(fill="both", expand=True)

        self.load_enrollment_records()

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

        tree_frame = tk.Frame(
            table_frame,
            bg="#FFFFFF"
        )
        tree_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15)
        )

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

        self._populate_records()

        tk.Button(
            table_frame, text="Drop Selected Enrollment", command=self.drop_selected,
            font=("Arial", 10, "bold"), bg="#DC3545", fg="#FFFFFF",
            activebackground="#B02A37", activeforeground="#FFFFFF", relief="flat",
            padx=15, pady=8, cursor="hand2"
        ).pack(anchor="e", padx=15, pady=(0, 15))

    def _populate_records(self):
        self.enrollment_table.delete(*self.enrollment_table.get_children())
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
                iid=f"{record['student_id']}::{record['course_code']}",
                values=(
                    student_text,
                    course_text,
                    record.get("timestamp") or ""
                )
            )

    def drop_selected(self):
        selected = self.enrollment_table.selection()
        if not selected:
            messagebox.showwarning("No Enrollment Selected", "Select an enrollment to drop.",
                                   parent=self.frame.winfo_toplevel())
            return
        student_id, course_code = selected[0].split("::", 1)
        if not messagebox.askyesno("Confirm Drop", f"Drop {student_id} from {course_code}?",
                                   parent=self.frame.winfo_toplevel()):
            return
        try:
            self.enrollment_service.drop(student_id, course_code)
            self.load_enrollment_records()
            self._populate_records()
            if self.on_change:
                self.on_change()
        except (ValueError, OSError) as exc:
            messagebox.showerror("Enrollment", str(exc), parent=self.frame.winfo_toplevel())

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

        #scrollable enrolled courses container
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

        student = self.student_service.get(student_id)
        if student is None:
            self.search_result.config(
                text="Student not found.",
                fg="#DC3545"
            )
            return

        student_records = self.enrollment_service.for_student(student_id)
        student_name = student["name"]

        self.search_result.config(
            text="Student records found successfully.",
            fg="#16803C"
        )

        self.student_name_label.config(
            text=f"Student: {student_name}"
        )

        # Display all courses actually recorded for this student.
        for record in student_records:
            course = self.course_service.get(record["course_code"])
            course_name = course["title"] if course else "Unknown course"
            course_text = f"{record['course_code']} - {course_name}"

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
                text=f"Enrolled: {record.get('timestamp') or 'Date unavailable'}",
                font=("Arial", 9),
                bg="#F1F3F5",
                fg="#555555"
            ).pack(
                anchor="w",
                padx=10,
                pady=(0, 8)
            )

        self.course_canvas.yview_moveto(0)

    def load_enrollment_records(self):
        self.enrollment_records = []
        for enrollment in self.enrollment_service.all():
            student = self.student_service.get(enrollment["student_id"])
            course = self.course_service.get(enrollment["course_code"])
            self.enrollment_records.append({
                **enrollment,
                "student_name": student["name"] if student else "Unknown student",
                "course_name": course["title"] if course else "Unknown course",
            })
