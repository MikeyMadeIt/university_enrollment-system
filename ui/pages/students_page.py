import tkinter as tk
from tkinter import ttk, messagebox
from services.student_service import StudentService
from ui.components.dialogs.student_dialogs import StudentRegistrationDialog, StudentInformationDialog

class StudentsPage:
    def __init__(self, parent):
        self.parent = parent
        self.service = StudentService()
        self.frame = tk.Frame(parent, bg="#F1F3F5")
        self.frame.pack(fill="both", expand=True)
        self._build()
        self.refresh()

    def _build(self):
        tk.Label(self.frame, text="Students", font=("Arial", 22, "bold"),
                 bg="#F1F3F5", fg="#07549C").pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(self.frame, text="Manage student records and information",
                 font=("Arial", 10), bg="#F1F3F5", fg="#555555"
                 ).pack(anchor="w", padx=25)

        sf = tk.Frame(self.frame, bg="#F1F3F5")
        sf.pack(fill="x", padx=25, pady=15)
        self.search_entry = tk.Entry(sf, font=("Arial", 11), relief="solid", bd=1)
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        tk.Button(sf, text="Search", bg="#07549C", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=25, pady=8, command=self.search_student
                  ).pack(side="right")

        self.search_result = tk.Label(self.frame, text="", font=("Arial", 9),
                                       bg="#F1F3F5", fg="#DC3545")
        self.search_result.pack(anchor="w", padx=25, pady=(0, 5))

        tf = tk.Frame(self.frame, bg="white", relief="solid", bd=1)
        tf.pack(fill="both", expand=True, padx=25, pady=(0, 10))
        self.tree = ttk.Treeview(tf, columns=("sid", "name"),
                                  show="headings", height=12)
        self.tree.heading("sid", text="Student ID")
        self.tree.heading("name", text="Student Name")
        self.tree.column("sid", width=150, anchor="center")
        self.tree.column("name", width=400, anchor="w")
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", padx=(0, 10), pady=10)

        self.tree.bind("<Double-1>", self.open_student_info)

        btn = tk.Frame(self.frame, bg="#F1F3F5")
        btn.pack(fill="x", padx=25, pady=(0, 20))

        tk.Button(btn, text="Delete Student", bg="#DC3545", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=self.delete_student
                  ).pack(side="right", padx=(10, 0))
        tk.Button(btn, text="+ Add Student", bg="#07549C", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=self.open_add_dialog
                  ).pack(side="right", padx=(10, 0))
        tk.Button(btn, text="View Info", bg="#6C757D", fg="white", font=("Arial", 10, "bold"),
                  relief="flat", padx=20, pady=8, command=lambda: self.open_student_info(None)
                  ).pack(side="right")

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for sid, info in self.service.sorted_students():
            self.tree.insert("", "end", values=(sid, info["name"]))
        self.search_result.config(text="") # Clear search status

    def search_student(self):
        q = self.search_entry.get().strip()
        if not q:
            self.search_result.config(text="Please enter a Student ID.", fg="#DC3545")
            return

        # returns just the info dict, e.g. {"name": "John", "completed_courses": []}
        result = self.service.search_by_id(q)

        for i in self.tree.get_children():
            self.tree.delete(i)

        if result is None:
            self.search_result.config(text="Student not found.", fg="#DC3545")
        else:
            # FIX: result is the info dict, not a tuple
            self.search_result.config(text="Student found successfully.", fg="#16803C")
            self.tree.insert("", "end", values=(q, result["name"]))

    def open_add_dialog(self):
        StudentRegistrationDialog(self.frame, on_success=self.refresh)

    def open_student_info(self, event):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Please select a student first.")
            return
        sid = self.tree.item(sel[0], "values")[0]
        StudentInformationDialog(self.frame, sid, on_refresh=self.refresh)

    def delete_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Student Selected", "Please select a student.")
            return
        sid = self.tree.item(sel[0], "values")[0]
        ok, msg = self.service.delete_student(sid)
        if ok:
            self.refresh()
        else:
            messagebox.showerror("Error", msg)
