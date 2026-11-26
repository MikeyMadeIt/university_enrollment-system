import tkinter as tk
from tkinter import ttk


class PrerequisitesPage:
    def __init__(self, parent, course_service, enrollment_service):
        self.courses, self.enrollments = course_service, enrollment_service
        frame = ttk.Frame(parent, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Prerequisite graph", font=("Arial", 21, "bold")).pack(anchor="w")
        controls = ttk.Frame(frame)
        controls.pack(fill="x", pady=12)
        self.code = tk.StringVar()
        ttk.Combobox(controls, textvariable=self.code, state="readonly", width=22,
                     values=[course["course_code"] for course in course_service.all()]).pack(side="left")
        ttk.Button(controls, text="DFS", command=self.show_dfs).pack(side="left", padx=5)
        ttk.Button(controls, text="BFS", command=self.show_bfs).pack(side="left")
        ttk.Button(controls, text="Topological order", command=self.show_order).pack(side="left", padx=5)
        self.output = tk.Text(frame, height=18, wrap="word", state="disabled")
        self.output.pack(fill="both", expand=True)
        self._write("Select a course to traverse dependent courses.")

    def _write(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", text)
        self.output.configure(state="disabled")

    def show_dfs(self):
        self._write(str(self.enrollments.prerequisite_dfs(self.code.get())))

    def show_bfs(self):
        self._write(f"Order: {self.enrollments.prerequisite_bfs(self.code.get())}\nLevels: {self.enrollments.prerequisite_levels(self.code.get())}")

    def show_order(self):
        self._write(str(self.enrollments.prerequisite_order()))
