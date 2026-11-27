import tkinter as tk
from tkinter import ttk, messagebox
from services.student_service import StudentService
from services.course_service import CourseService

class StudentRegistrationDialog:
    def __init__(self, parent, on_success=None):
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Register Student")
        self.window.geometry("500x350")
        self.window.configure(bg="white")
        self.window.transient(parent)

        # FIX: Force draw before grab
        self.window.update()
        self.window.grab_set()
        self.window.lift()

        tk.Label(self.window, text="Register Student", font=("Arial", 18, "bold"),
                 bg="white", fg="#07549C").pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(self.window, text="Enter the student's information.", font=("Arial", 10),
                 bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 15))

        tk.Label(self.window, text="Student ID", font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=20)
        self.id_entry = tk.Entry(self.window, font=("Arial", 11), relief="solid", bd=1)
        self.id_entry.pack(fill="x", padx=20, pady=(5, 15), ipady=5)

        tk.Label(self.window, text="Full Name", font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=20)
        self.name_entry = tk.Entry(self.window, font=("Arial", 11), relief="solid", bd=1)
        self.name_entry.pack(fill="x", padx=20, pady=(5, 20), ipady=5)

        btn_frame = tk.Frame(self.window, bg="white")
        btn_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(btn_frame, text="Cancel", font=("Arial", 10), bg="#E9ECEF",
                  relief="flat", padx=20, pady=8, command=self.window.destroy).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Register Student", font=("Arial", 10, "bold"),
                  bg="#07549C", fg="white", relief="flat", padx=20, pady=8,
                  command=self.register).pack(side="right")

    def register(self):
        sid = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        ok, msg = StudentService().add_student(sid, name)
        if ok:
            messagebox.showinfo("Success", msg, parent=self.window)
            if self.on_success:
                self.on_success()
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self.window)

class StudentInformationDialog:
    def __init__(self, parent, student_id, on_refresh=None):
        self.student_id = student_id
        self.on_refresh = on_refresh
        self.window = tk.Toplevel(parent)
        self.window.title("Student Information")
        self.window.geometry("500x400")
        self.window.configure(bg="white")
        self.window.transient(parent)

        # FIX: Force draw before grab
        self.window.update()
        self.window.grab_set()
        self.window.lift()

        self.build()

    def build(self):
        for w in self.window.winfo_children():
            w.destroy()

        student = StudentService().get_student(self.student_id)
        if not student:
            return

        tk.Label(self.window, text="Student Information", font=("Arial", 18, "bold"),
                 bg="white", fg="#07549C").pack(anchor="w", padx=20, pady=(20, 15))

        tk.Label(self.window, text="Student ID", font=("Arial", 10, "bold"),
                 bg="white", fg="#333").pack(anchor="w", padx=20)
        tk.Label(self.window, text=self.student_id, font=("Arial", 12),
                 bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 15))

        tk.Label(self.window, text="Full Name", font=("Arial", 10, "bold"),
                 bg="white", fg="#333").pack(anchor="w", padx=20)
        tk.Label(self.window, text=student["name"], font=("Arial", 12),
                 bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 15))

        tk.Label(self.window, text="Completed Courses", font=("Arial", 10, "bold"),
                 bg="white", fg="#333").pack(anchor="w", padx=20)
        courses_text = ", ".join(sorted(student["completed_courses"])) or "None"
        tk.Label(self.window, text=courses_text, font=("Arial", 12),
                 bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 20))

        tk.Button(self.window, text="+ Add Completed Course", font=("Arial", 10),
                  bg="#07549C", fg="white", relief="flat", padx=15, pady=8,
                  command=self.open_add_course).pack(anchor="w", padx=20)

        tk.Button(self.window, text="Close", font=("Arial", 10), bg="#E9ECEF",
                  relief="flat", padx=20, pady=8, command=self.window.destroy
                  ).pack(anchor="e", padx=20, pady=20)

    def open_add_course(self):
        AddCompletedCourseDialog(self.window, self.student_id, on_success=self.build)

class AddCompletedCourseDialog:
    def __init__(self, parent, student_id, on_success=None):
        self.student_id = student_id
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Add Completed Course")
        self.window.geometry("450x250")
        self.window.configure(bg="white")
        self.window.transient(parent)

        # FIX: Force draw before grab
        self.window.update()
        self.window.grab_set()
        self.window.lift()

        tk.Label(self.window, text="Add Completed Course", font=("Arial", 16, "bold"),
                 bg="white", fg="#07549C").pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(self.window, text="Select a course to add to the student's records.",
                 font=("Arial", 10), bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 15))

        tk.Label(self.window, text="Course", font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=20)

        self.course_var = tk.StringVar()
        self.combo = ttk.Combobox(self.window, textvariable=self.course_var, state="readonly")
        self.combo.pack(fill="x", padx=20, pady=(5, 20), ipady=5)

        cs = CourseService()
        courses = cs.get_all_courses()
        self.combo["values"] = [f"{c} - {i['name']}" for c, i in courses.items()]
        if self.combo["values"]:
            self.combo.current(0)

        btn_frame = tk.Frame(self.window, bg="white")
        btn_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(btn_frame, text="Cancel", font=("Arial", 10), bg="#E9ECEF",
                  relief="flat", padx=20, pady=8, command=self.window.destroy).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Add Course", font=("Arial", 10, "bold"),
                  bg="#07549C", fg="white", relief="flat", padx=20, pady=8,
                  command=self.add_course).pack(side="right")

    def add_course(self):
        selection = self.course_var.get().strip()
        if not selection:
            return
        code = selection.split(" - ")[0].strip()
        ok, msg = StudentService().mark_completed(self.student_id, code)
        if ok:
            if self.on_success:
                self.on_success()
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self.window)
