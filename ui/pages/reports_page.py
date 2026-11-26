import tkinter as tk
from tkinter import ttk


class ReportsPage:
    def __init__(self, parent, report_service):
        self.reports = report_service
        frame = ttk.Frame(parent, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Enrollment report", font=("Arial", 21, "bold")).pack(anchor="w")
        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=12)
        self.sort_key = tk.StringVar(value="student_name")
        ttk.Label(controls, text="Sort by").pack(side="left")
        ttk.Combobox(controls, textvariable=self.sort_key, state="readonly", width=18,
                     values=("student_name", "course_name", "student_id", "course_code")).pack(side="left", padx=6)
        ttk.Button(controls, text="Refresh", command=self.refresh).pack(side="left")
        columns = ("student_id", "student_name", "course_code", "course_name", "timestamp")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, width in zip(columns, (120, 190, 120, 220, 190)):
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.reports.enrollment_report(self.sort_key.get()):
            self.tree.insert("", "end", values=(row["student_id"], row["student_name"], row["course_code"], row["course_name"], row.get("timestamp") or ""))
