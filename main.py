"""Launch the existing QCU UI with real services wired in."""

import os
import tkinter as tk

from storage.json_storage import JsonStorage
from data_structures.structures import (
    StudentCollection, CourseCollection, EnrollmentCollection,
)
from services.student_service import StudentService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService
from utils.seed import ensure_seed_data
from ui.main_window import MainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def main():
    storage = JsonStorage(DATA_DIR)
    ensure_seed_data(storage)

    student_service = StudentService(
        storage, StudentCollection(storage.load("students.json", [])))
    course_service = CourseService(
        storage, CourseCollection(storage.load("courses.json", [])))
    enrollment_service = EnrollmentService(
        storage,
        EnrollmentCollection(storage.load("enrollments.json", [])),
        student_service,
        course_service,
    )

    root = tk.Tk()
    app = MainWindow(root, student_service, course_service, enrollment_service)
    root.mainloop()


if __name__ == "__main__":
    main()