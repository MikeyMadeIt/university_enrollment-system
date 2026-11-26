import tkinter as tk
from tkinter import ttk

BLUE, PAGE, WHITE = "#07549C", "#F1F3F5", "#FFFFFF"


class ReportsPage:
    def __init__(self, parent, report_service):
        self.reports = report_service
        frame = tk.Frame(parent, bg=PAGE)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Enrollment Report", font=("Arial", 22, "bold"),
                 bg=PAGE, fg=BLUE).pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(frame, text="Review student course registrations",
                 font=("Arial", 10), bg=PAGE, fg="#555555").pack(anchor="w", padx=25)
        panel = tk.Frame(frame, bg=WHITE, highlightbackground="#D9DDE2", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=25, pady=20)
        controls = tk.Frame(panel, bg=WHITE)
        controls.pack(fill="x", padx=15, pady=15)
        self.sort_key = tk.StringVar(value="student_name")
        tk.Label(controls, text="Sort by", font=("Arial", 10, "bold"), bg=WHITE,
                 fg="#333333").pack(side="left")
        ttk.Combobox(controls, textvariable=self.sort_key, state="readonly", width=18,
                     values=("student_name", "course_name", "student_id", "course_code")).pack(side="left", padx=6)
        tk.Button(controls, text="Refresh", command=self.refresh, font=("Arial", 10, "bold"),
                  bg=BLUE, fg=WHITE, activebackground="#06447D", activeforeground=WHITE,
                  relief="flat", padx=15, pady=8, cursor="hand2").pack(side="left")
        columns = ("student_id", "student_name", "course_code", "course_name", "timestamp")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, width in zip(columns, (120, 190, 120, 220, 190)):
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=width, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.reports.enrollment_report(self.sort_key.get()):
            self.tree.insert("", "end", values=(row["student_id"], row["student_name"], row["course_code"], row["course_name"], row.get("timestamp") or ""))
