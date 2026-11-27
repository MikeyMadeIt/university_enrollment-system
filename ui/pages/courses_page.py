import tkinter as tk
from tkinter import ttk, messagebox
from services.course_service import CourseService
from ui.components.dialogs.course_dialogs import AddCourseDialog, EnrolledStudentsDialog

class CoursesPage:
    def __init__(self, parent):
        self.parent = parent
        self.service = CourseService()
        self.frame = tk.Frame(parent, bg="#F1F3F5")
        self.frame.pack(fill="both", expand=True)
        self._build()
        self.refresh()

    def _build(self):
        tk.Label(self.frame, text="Courses", font=("Arial", 22, "bold"),
                 bg="#F1F3F5", fg="#07549C").pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame, text="Manage available courses and course information",
                 font=("Arial", 10), bg="#F1F3F5", fg="#555555"
                 ).pack(anchor="w", padx=25)

        sf = tk.Frame(self.frame, bg="#F1F3F5")
        sf.pack(fill="x", padx=25, pady=15)
        self.search_entry = tk.Entry(sf, font=("Arial", 11), relief="solid", bd=1)
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        tk.Button(sf, text="Search", bg="#07549C", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=25, pady=8, command=self.search_course
                  ).pack(side="right")

        self.search_result = tk.Label(self.frame, text="", font=("Arial", 9),
                                       bg="#F1F3F5", fg="#DC3545")
        self.search_result.pack(anchor="w", padx=25, pady=(0, 5))

        tf = tk.Frame(self.frame, bg="white", relief="solid", bd=1)
        tf.pack(fill="both", expand=True, padx=25, pady=(0, 10))
        self.tree = ttk.Treeview(tf, columns=("code", "name", "cap", "enrolled"),
                                  show="headings", height=12)
        self.tree.heading("code", text="Course Code")
        self.tree.heading("name", text="Course Name")
        self.tree.heading("cap", text="Capacity")
        self.tree.heading("enrolled", text="Enrolled")
        self.tree.column("code", width=100, anchor="center")
        self.tree.column("name", width=350, anchor="w")
        self.tree.column("cap", width=100, anchor="center")
        self.tree.column("enrolled", width=100, anchor="center")
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree.bind("<Double-1>", self.open_roster)

        btn = tk.Frame(self.frame, bg="#F1F3F5")
        btn.pack(fill="x", padx=25, pady=(0, 20))
        tk.Button(btn, text="+ Add Course", bg="#07549C", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=self.open_add_dialog
                  ).pack(side="right", padx=(10, 0))
        tk.Button(btn, text="Delete Course", bg="#DC3545", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=self.delete_course
                  ).pack(side="right", padx=(10, 0))
        tk.Button(btn, text="View Roster", bg="#6C757D", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=lambda: self.open_roster(None)
                  ).pack(side="right")

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for code, info in self.service.sorted_courses():
            self.tree.insert("", "end", values=(
                code, info["name"], info["capacity"], len(info["enrolled"])))

    def search_course(self):
        q = self.search_entry.get().strip()
        if not q:
            self.search_result.config(text="Please enter a Course Code.", fg="#DC3545")
            return
        result = self.service.search_by_code(q)
        for i in self.tree.get_children():
            self.tree.delete(i)
        if result is None:
            self.search_result.config(text="Course not found.", fg="#DC3545")
        else:
            info = result
            self.search_result.config(text="Course found.", fg="#16803C")
            self.tree.insert("", "end", values=(
                q.upper(), info["name"], info["capacity"], len(info["enrolled"])))

    def open_add_dialog(self):
        AddCourseDialog(self.frame, on_success=self.refresh)

    def delete_course(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Course Selected", "Please select a course.")
            return
        code = self.tree.item(sel[0], "values")[0]
        if not messagebox.askyesno(
                "Delete Course",
                f"Delete {code}? Courses with enrollments or dependent courses cannot be deleted."):
            return
        ok, msg = self.service.delete_course(code)
        if ok:
            self.refresh()
            self.search_result.config(text=msg, fg="#16803C")
        else:
            messagebox.showerror("Cannot Delete Course", msg)

    def open_roster(self, event):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Please select a course first.")
            return
        code = self.tree.item(sel[0], "values")[0]
        EnrolledStudentsDialog(self.frame, code, on_refresh=self.refresh)
