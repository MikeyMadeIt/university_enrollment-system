import tkinter as tk
from tkinter import ttk, messagebox
from services.course_service import CourseService
from services.student_service import StudentService
from services.enrollment_service import EnrollmentService

class AddCourseDialog:
    def __init__(self, parent, on_success=None):
        self.on_success = on_success
        self.window = tk.Toplevel(parent)
        self.window.title("Add Course")
        self.window.geometry("500x550")
        self.window.configure(bg="white")
        self.window.transient(parent)

        # FIX: Force draw before grab
        self.window.update()
        self.window.grab_set()
        self.window.lift()

        tk.Label(self.window, text="Add Course", font=("Arial", 18, "bold"),
                 bg="white", fg="#07549C").pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(self.window, text="Enter the course information.", font=("Arial", 10),
                 bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 15))

        tk.Label(self.window, text="Course Code", font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=20)
        self.code_entry = tk.Entry(self.window, font=("Arial", 11), relief="solid", bd=1)
        self.code_entry.pack(fill="x", padx=20, pady=(5, 10), ipady=4)

        tk.Label(self.window, text="Course Name", font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=20)
        self.name_entry = tk.Entry(self.window, font=("Arial", 11), relief="solid", bd=1)
        self.name_entry.pack(fill="x", padx=20, pady=(5, 10), ipady=4)

        tk.Label(self.window, text="Course Capacity", font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=20)
        self.capacity_entry = tk.Entry(self.window, font=("Arial", 11), relief="solid", bd=1)
        self.capacity_entry.pack(fill="x", padx=20, pady=(5, 10), ipady=4)

        tk.Label(self.window, text="Prerequisites", font=("Arial", 10, "bold"),
                 bg="white").pack(anchor="w", padx=20)

        list_frame = tk.Frame(self.window, bg="white", relief="solid", bd=1)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        canvas = tk.Canvas(list_frame, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.no_prereq_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.scrollable_frame, text="No prerequisites", variable=self.no_prereq_var,
                       bg="white", command=self.toggle_all).pack(anchor="w", pady=2)

        self.prereq_vars = {}
        courses = CourseService().get_all_courses()
        for code, info in courses.items():
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.scrollable_frame, text=f"{code} - {info['name']}",
                                variable=var, bg="white", command=self.check_if_none)
            cb.pack(anchor="w", pady=2)
            self.prereq_vars[code] = var

        btn_frame = tk.Frame(self.window, bg="white")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Button(btn_frame, text="Cancel", font=("Arial", 10), bg="#E9ECEF",
                  relief="flat", padx=20, pady=8, command=self.window.destroy).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Add Course", font=("Arial", 10, "bold"),
                  bg="#07549C", fg="white", relief="flat", padx=20, pady=8,
                  command=self.add_course).pack(side="right")

    def toggle_all(self):
        if self.no_prereq_var.get():
            for var in self.prereq_vars.values():
                var.set(False)

    def check_if_none(self):
        if any(var.get() for var in self.prereq_vars.values()):
            self.no_prereq_var.set(False)
        else:
            self.no_prereq_var.set(True)

    def add_course(self):
        code = self.code_entry.get().strip().upper()
        name = self.name_entry.get().strip()
        cap = self.capacity_entry.get().strip()
        prereqs = [c for c, v in self.prereq_vars.items() if v.get()]

        ok, msg = CourseService().add_course(code, name, cap, prereqs)
        if ok:
            messagebox.showinfo("Success", msg, parent=self.window)
            if self.on_success:
                self.on_success()
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg, parent=self.window)

class EnrolledStudentsDialog:
    def __init__(self, parent, course_code, on_refresh=None):
        self.course_code = course_code
        self.on_refresh = on_refresh
        self.course_service = CourseService()
        self.student_service = StudentService()
        self.enrollment_service = EnrollmentService(
            student_service=self.student_service,
            course_service=self.course_service)
        self.window = tk.Toplevel(parent)
        self.window.title("Enrolled Students")
        self.window.geometry("600x500")
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

        cs = self.course_service
        ss = self.student_service
        course = cs.get_course(self.course_code)
        if not course:
            return

        tk.Label(self.window, text="Enrolled Students", font=("Arial", 18, "bold"),
                 bg="white", fg="#07549C").pack(anchor="w", padx=20, pady=(20, 5))
        tk.Label(self.window, text=f"{self.course_code} - {course['name']}",
                 font=("Arial", 10), bg="white", fg="#555").pack(anchor="w", padx=20, pady=(0, 15))

        tk.Label(self.window, text="Course Prerequisites", font=("Arial", 10, "bold"),
                 bg="white", fg="#333").pack(anchor="w", padx=20)
        prereq_frame = tk.Frame(self.window, bg="white", relief="solid", bd=1)
        prereq_frame.pack(fill="x", padx=20, pady=(5, 15))
        prereq_text = ", ".join(sorted(course["prerequisites"])) or "No prerequisites"
        tk.Label(prereq_frame, text=prereq_text, font=("Arial", 10), bg="white",
                 fg="#555", anchor="w").pack(fill="x", padx=10, pady=5)

        tk.Label(self.window, text="Enrolled Students", font=("Arial", 10, "bold"),
                 bg="white", fg="#333").pack(anchor="w", padx=20)

        tree_frame = tk.Frame(self.window, bg="white", relief="solid", bd=1)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.tree = ttk.Treeview(tree_frame, columns=("sid", "name"), show="headings", height=8)
        self.tree.heading("sid", text="Student ID")
        self.tree.heading("name", text="Student Name")
        self.tree.column("sid", width=150)
        self.tree.column("name", width=300)

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="right", fill="y", padx=(0,10), pady=10)

        enrolled = cs.get_roster(self.course_code)
        for sid in enrolled:
            student = ss.get_student(sid)
            name = student["name"] if student else "(missing)"
            self.tree.insert("", "end", values=(sid, name))

        btn_frame = tk.Frame(self.window, bg="white")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        tk.Button(btn_frame, text="Drop Student", font=("Arial", 10, "bold"),
                  bg="#DC3545", fg="white", relief="flat", padx=15, pady=8,
                  command=self.drop_student).pack(side="left")
        tk.Button(btn_frame, text="Close", font=("Arial", 10), bg="#E9ECEF",
                  relief="flat", padx=20, pady=8, command=self.window.destroy
                  ).pack(side="right")

    def drop_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a student to drop.", parent=self.window)
            return
        sid = self.tree.item(sel[0], "values")[0]
        ok, msg = self.enrollment_service.drop(sid, self.course_code)
        if ok:
            if self.on_refresh:
                self.on_refresh()
            self.build()
        else:
            messagebox.showerror("Error", msg, parent=self.window)
