
import tkinter as tk


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


# ======================================================

class ViewStudentDialog:

    def __init__(self, parent, student_id, student_name, completed_courses):
        self.window = tk.Toplevel(parent)
        self.window.title("Student Information")
        self.window.geometry("450x350")
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
        title.pack(anchor="w", padx=25, pady=(25, 20))

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
        id_value.pack(anchor="w", padx=25, pady=(5, 15))

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
        name_value.pack(anchor="w", padx=25, pady=(5, 15))

        courses_label = tk.Label(
            self.window,
            text="Completed Courses",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        courses_label.pack(anchor="w", padx=25)

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
        courses_value.pack(anchor="w", padx=25, pady=(5, 20))

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
        close_button.pack(anchor="e", padx=25, pady=(0, 20))


# ======================================================
#for courses_page.py
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

        # Course Name
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
        prerequisite_label.pack(anchor="w", padx=25, pady=(0, 5))

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

        # Existing courses as prerequisite options
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

# ======================================================

# Testing code 4 AddCourseDialog
if __name__ == "__main__":

    root = tk.Tk()
    root.title("QCU Enrollment System")
    root.geometry("800x600")

    sample_courses = {
        "CS101": {
            "name": "Introduction to Computing",
            "capacity": 40,
            "enrolled": set(),
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

    AddCourseDialog(root, sample_courses)
    root.mainloop()

#testing code for ViewStudentDialog
#if __name__ == "__main__":
#    root = tk.Tk()
#    root.geometry("800x500")

#    ViewStudentDialog(
#        root,
#        "2026-001",
#        "Lopez, Dhan Paul",
#        {"CS101", "CS102", "CS103", "CS104", "CS105", "CS106", "CS107", "CS108", "CS109",}
#    )

#    root.mainloop()

#testing code for StudentRegistrationDialog
#if __name__ == "__main__":
#    root = tk.Tk()
#    root.geometry("800x500")
#
#    StudentRegistrationDialog(root)
#
#    root.mainloop()
#


