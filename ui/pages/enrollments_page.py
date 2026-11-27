import tkinter as tk
from tkinter import ttk, messagebox
from services.student_service import StudentService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService

class EnrollmentsPage:
    def __init__(self, parent):
        self.parent = parent
        self.student_service = StudentService()
        self.course_service = CourseService()
        self.service = EnrollmentService(
            student_service=self.student_service,
            course_service=self.course_service)

        self.current_student_id = None
        self.course_vars = {}

        self.frame = tk.Frame(parent, bg="#F1F3F5")
        self.frame.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        tk.Label(self.frame, text="Student Enrollment", font=("Arial", 22, "bold"),
                 bg="#F1F3F5", fg="#07549C").pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame, text="Enter a student ID and select courses for enrollment",
                 font=("Arial", 10), bg="#F1F3F5", fg="#555555"
                 ).pack(anchor="w", padx=25)

        # --- Student Info Section ---
        s_frame = tk.Frame(self.frame, bg="white", relief="solid", bd=1)
        s_frame.pack(fill="x", padx=25, pady=15)

        tk.Label(s_frame, text="Student Information", font=("Arial", 14, "bold"),
                 bg="white", fg="#07549C").pack(anchor="w", padx=20, pady=(15, 10))

        sf = tk.Frame(s_frame, bg="white")
        sf.pack(fill="x", padx=20, pady=(0, 15))

        tk.Label(sf, text="Student ID", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
        inner = tk.Frame(sf, bg="white")
        inner.pack(fill="x", pady=(5, 0))

        self.id_entry = tk.Entry(inner, font=("Arial", 11), relief="solid", bd=1)
        self.id_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        tk.Button(inner, text="Check Student", bg="#07549C", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=self.check_student).pack(side="right")

        self.status_label = tk.Label(sf, text="", font=("Arial", 10), bg="white")
        self.status_label.pack(anchor="w", pady=(10, 0))

        # --- Course Selection Section ---
        c_frame = tk.Frame(self.frame, bg="white", relief="solid", bd=1)
        c_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))

        tk.Label(c_frame, text="Select Courses", font=("Arial", 14, "bold"),
                 bg="white", fg="#07549C").pack(anchor="w", padx=20, pady=(15, 5))
        tk.Label(c_frame, text="Select one or more courses from the available list below.",
                 font=("Arial", 10), bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 10))

        # Scrollable checkboxes
        list_frame = tk.Frame(c_frame, bg="white")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.check_frame = tk.Frame(canvas, bg="white")

        self.check_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.check_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_courses()

        # --- Submit Button ---
        btn_frame = tk.Frame(self.frame, bg="#F1F3F5")
        btn_frame.pack(fill="x", padx=25, pady=(0, 20))
        tk.Button(btn_frame, text="Submit Enrollment", bg="#07549C", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=self.submit_enrollment).pack(side="right")

    def load_courses(self):
        for w in self.check_frame.winfo_children():
            w.destroy()
        self.course_vars.clear()

        courses = self.course_service.get_all_courses()
        for code, info in courses.items():
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.check_frame, text=f"{code} - {info['name']}",
                                variable=var, bg="white", font=("Arial", 11))
            cb.pack(anchor="w", pady=5)
            self.course_vars[code] = var

    def check_student(self):
        sid = self.id_entry.get().strip()
        if not sid:
            return
        student = self.student_service.get_student(sid)
        if student:
            self.current_student_id = sid
            self.status_label.config(text=f"Student found successfully.\nStudent Name: {student['name']}",
                                     fg="#16803C", font=("Arial", 10, "bold"))
        else:
            self.current_student_id = None
            self.status_label.config(text="Student not found.", fg="#DC3545", font=("Arial", 10))

    def submit_enrollment(self):
        if not self.current_student_id:
            messagebox.showwarning("Warning", "Please check a valid student first.")
            return

        selected_courses = [code for code, var in self.course_vars.items() if var.get()]
        if not selected_courses:
            messagebox.showwarning("Warning", "Please select at least one course.")
            return

        success_count = 0
        errors = []

        for code in selected_courses:
            ok, msg = self.service.enroll(self.current_student_id, code)
            if ok:
                success_count += 1
            else:
                errors.append(f"{code}: {msg}")

        if success_count > 0:
            messagebox.showinfo("Success", f"Successfully enrolled in {success_count} course(s).")
        if errors:
            messagebox.showerror("Enrollment Errors", "The following failed:\n\n" + "\n".join(errors))

        # Uncheck all boxes and refresh
        for var in self.course_vars.values():
            var.set(False)
        self.load_courses()
