"""Tkinter application launcher; page behavior lives in the page modules."""

import tkinter as tk

from ui.main_window import MainWindow


def run_app(student_service, course_service, enrollment_service, report_service):
    root = tk.Tk()
    MainWindow(root, student_service, course_service, enrollment_service, report_service)
    root.mainloop()
