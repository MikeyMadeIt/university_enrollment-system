import tkinter as tk

class StudentRegistrationDialog:

    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Register Student")
        self.window.geometry("450x370")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        # Make dialog appear in front
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

        # Button container
        button_frame = tk.Frame(
            self.window,
            bg="#FFFFFF"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=(5, 20)
        )

        # Cancel button
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

        # Register button
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
#====================================================

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

        # Dialog heading
        title = tk.Label(
            self.window,
            text="Student Information",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(25, 20))

        # Student ID
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

        # Full Name
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

        # Completed Courses
        courses_label = tk.Label(
            self.window,
            text="Completed Courses",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#333333"
        )
        courses_label.pack(anchor="w", padx=25)

        courses_text = ", ".join(sorted(completed_courses)) if completed_courses else "None"

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

        # Close button
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

#==============================================================

#for testing

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x500")

    ViewStudentDialog(
        root,
        "2026-001",
        "Lopez, Dhan Paul",
        {"CS101", "CS102", "CS103", "CS104", "CS105", "CS106", "CS107", "CS108", "CS109",}
    )

    root.mainloop()

#if __name__ == "__main__":
#    root = tk.Tk()
#    root.geometry("800x500")
#
#    StudentRegistrationDialog(root)
#
#    root.mainloop()
#


