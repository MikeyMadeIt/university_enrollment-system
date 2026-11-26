
import tkinter as tk
from tkinter import ttk


class EnrollmentsPage:

    def __init__(self, parent, student_service, course_service,
                 enrollment_service, on_change=None):
        self.parent = parent
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service
        self.on_change = on_change

        # Main page frame
        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )
        self.frame.pack(fill="both", expand=True)

        self.load_courses()

        self.create_header()
        self.create_student_selection()
        self.create_course_selection()
        self.create_submit_button()

    def create_header(self):

        title = tk.Label(
            self.frame,
            text="Student Enrollment",
            font=("Arial", 22, "bold"),
            bg="#F1F3F5",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(25, 5))

        subtitle = tk.Label(
            self.frame,
            text="Enter a student ID and select a course for enrollment",
            font=("Arial", 10),
            bg="#F1F3F5",
            fg="#555555"
        )
        subtitle.pack(anchor="w", padx=25)

    def create_student_selection(self):

        student_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF"
        )
        student_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        section_title = tk.Label(
            student_frame,
            text="Student Information",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        section_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 10)
        )

        tk.Label(
            student_frame,
            text="Student ID",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 5)
        )

        input_frame = tk.Frame(
            student_frame,
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

        check_button = tk.Button(
            input_frame,
            text="Check Student",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.check_student
        )
        check_button.pack(side="right")

        self.student_result = tk.Label(
            student_frame,
            text="",
            font=("Arial", 10),
            bg="#FFFFFF",
            fg="#16803C"
        )
        self.student_result.pack(
            anchor="w",
            padx=15,
            pady=(12, 0)
        )

        self.student_name_label = tk.Label(
            student_frame,
            text="",
            font=("Arial", 11, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        self.student_name_label.pack(
            anchor="w",
            padx=15,
            pady=(5, 15)
        )

    def create_course_selection(self):

        course_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF"
        )
        course_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        section_title = tk.Label(
            course_frame,
            text="Select Course",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        section_title.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        description = tk.Label(
            course_frame,
            text="Select one course from the available courses below.",
            font=("Arial", 9),
            bg="#FFFFFF",
            fg="#555555"
        )
        description.pack(
            anchor="w",
            padx=15,
            pady=(0, 10)
        )

        list_container = tk.Frame(
            course_frame,
            bg="#FFFFFF"
        )
        list_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.course_canvas = tk.Canvas(
            list_container,
            bg="#FFFFFF",
            height=150,
            highlightthickness=0
        )
        self.course_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            list_container,
            orient="vertical",
            command=self.course_canvas.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.course_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.course_list_frame = tk.Frame(
            self.course_canvas,
            bg="#FFFFFF"
        )

        self.course_canvas_window = self.course_canvas.create_window(
            (0, 0),
            window=self.course_list_frame,
            anchor="nw"
        )

        self.course_list_frame.bind(
            "<Configure>",
            self.update_course_scroll
        )

        self.course_canvas.bind(
            "<Configure>",
            self.update_course_canvas_width
        )

        self.selected_course = tk.StringVar(value="")

        for course_code, details in self.courses.items():

            course_text = (
                f"{course_code} - {details['name']}"
            )

            course_radio = tk.Radiobutton(
                self.course_list_frame,
                text=course_text,
                variable=self.selected_course,
                value=course_code,
                font=("Arial", 10),
                bg="#FFFFFF",
                fg="#333333",
                activebackground="#FFFFFF",
                activeforeground="#07549C",
                selectcolor="#FFFFFF",
                anchor="w",
                padx=5,
                pady=5
            )
            course_radio.pack(
                fill="x",
                anchor="w"
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

    def create_submit_button(self):

        button_frame = tk.Frame(
            self.frame,
            bg="#F1F3F5"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

        submit_button = tk.Button(
            button_frame,
            text="Submit Enrollment",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.submit_enrollment
        )
        submit_button.pack(side="right")

        self.enrollment_result = tk.Label(
            button_frame,
            text="",
            font=("Arial", 10, "bold"),
            bg="#F1F3F5",
            fg="#16803C"
        )
        self.enrollment_result.pack(
            side="left",
            pady=5
        )

    def check_student(self):

        student_id = self.student_id_entry.get().strip()

        if not student_id:
            self.student_result.config(
                text="Please enter a Student ID.",
                fg="#DC3545"
            )
            self.student_name_label.config(text="")
            return

        student = self.student_service.get(student_id)
        if not student:

            self.student_result.config(
                text="Student ID does not exist.",
                fg="#DC3545"
            )

            self.student_name_label.config(
                text=""
            )
        elif student:

            self.student_result.config(
                text="Student found successfully.",
                fg="#16803C"
            )

            self.student_name_label.config(
                text=f"Student Name: {student['name']}"
            )

        else:
            self.student_result.config(
                text="Please enter a Student ID.",
                fg="#DC3545"
            )

            self.student_name_label.config(
                text=""
            )

    def submit_enrollment(self):

        student_id = self.student_id_entry.get().strip()
        course_code = self.selected_course.get()

        #if both input empty show error
        if not student_id or not course_code:

            self.enrollment_result.config(
                text="Please enter a Student ID and select a course.",
                fg="#DC3545"
            )
        else:
            try:
                self.enrollment_service.enroll(student_id, course_code)
                self.enrollment_result.config(text="Enrollment submitted successfully!", fg="#16803C")
                if self.on_change:
                    self.on_change()
            except (ValueError, OSError) as exc:
                self.enrollment_result.config(text=f"Enrollment failed: {exc}", fg="#DC3545")

    def load_courses(self):
        self.courses = {
            course["course_code"]: course
            for course in self.course_service.all()
        }

# Temporary testing
if __name__ == "__main__":

    root = tk.Tk()
    root.title("QCU Enrollment System")
    root.geometry("1000x650")

    EnrollmentsPage(root)

    root.mainloop()
