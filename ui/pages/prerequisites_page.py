import tkinter as tk
from tkinter import ttk

BLUE, PAGE, WHITE = "#07549C", "#F1F3F5", "#FFFFFF"


class PrerequisitesPage:
    def __init__(self, parent, course_service, enrollment_service):
        self.courses, self.enrollments = course_service, enrollment_service
        frame = tk.Frame(parent, bg=PAGE)
        frame.pack(fill="both", expand=True)
        tk.Label(frame, text="Prerequisite Graph", font=("Arial", 22, "bold"),
                 bg=PAGE, fg=BLUE).pack(anchor="w", padx=25, pady=(25, 5))
        tk.Label(frame, text="Explore course dependencies and prerequisite order",
                 font=("Arial", 10), bg=PAGE, fg="#555555").pack(anchor="w", padx=25)
        panel = tk.Frame(frame, bg=WHITE, highlightbackground="#D9DDE2", highlightthickness=1)
        panel.pack(fill="both", expand=True, padx=25, pady=20)
        controls = tk.Frame(panel, bg=WHITE)
        controls.pack(fill="x", padx=15, pady=15)
        self.code = tk.StringVar()
        ttk.Combobox(controls, textvariable=self.code, state="readonly", width=22,
                     values=[course["course_code"] for course in course_service.all()]).pack(side="left")
        self._button(controls, "DFS", self.show_dfs).pack(side="left", padx=5)
        self._button(controls, "BFS", self.show_bfs).pack(side="left")
        self._button(controls, "Topological Order", self.show_order).pack(side="left", padx=5)
        self.output = tk.Text(panel, height=18, wrap="word", state="disabled", font=("Arial", 10),
                              bg=WHITE, fg="#333333", relief="solid", bd=1, padx=12, pady=10)
        self.output.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self._write("Select a course to traverse dependent courses.")

    @staticmethod
    def _button(parent, text, command):
        return tk.Button(parent, text=text, command=command, font=("Arial", 10, "bold"),
                         bg=BLUE, fg=WHITE, activebackground="#06447D", activeforeground=WHITE,
                         relief="flat", padx=15, pady=8, cursor="hand2")

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
