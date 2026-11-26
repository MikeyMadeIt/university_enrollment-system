import tkinter as tk

from ui.components.header import Header
from ui.components.sidebar import Sidebar
from ui.pages.courses_page import CoursesPage
from ui.pages.dashboard import Dashboard
from ui.pages.enrollments_page import EnrollmentsPage
from ui.pages.prerequisites_page import PrerequisitesPage
from ui.pages.reports_page import ReportsPage
from ui.pages.students_page import StudentsPage


class MainWindow:
    def __init__(self, root, student_service, course_service, enrollment_service, report_service):
        self.root = root
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service
        self.report_service = report_service
        root.title("QCU - Course Registration System")
        root.geometry("1280x800")
        root.minsize(950, 600)
        root.configure(bg="#F1F3F5")

        Header(root).pack(fill="x")
        body = tk.Frame(root, bg="#F1F3F5")
        body.pack(fill="both", expand=True)
        self.sidebar = Sidebar(body, self.show_page)
        self.sidebar.pack(side="left", fill="y")
        self.page_container = tk.Frame(body, bg="#F1F3F5")
        self.page_container.pack(side="left", fill="both", expand=True)
        self.show_page("Dashboard")

    def show_page(self, page_name):
        self.current_page = page_name
        for widget in self.page_container.winfo_children():
            widget.destroy()
        self.sidebar.set_active(page_name)
        args = {
            "Dashboard": (Dashboard, (self.student_service, self.course_service, self.enrollment_service)),
            "Students": (StudentsPage, (self.student_service, self.enrollment_service)),
            "Courses": (CoursesPage, (self.course_service, self.enrollment_service)),
            "Enrollments": (EnrollmentsPage, (self.student_service, self.course_service, self.enrollment_service)),
            "Prerequisites": (PrerequisitesPage, (self.course_service, self.enrollment_service)),
            "Reports": (ReportsPage, (self.report_service,)),
        }
        page_class, services = args[page_name]
        self.page = page_class(self.page_container, *services, on_change=self.refresh_pages) if page_name in {"Students", "Courses", "Enrollments"} else page_class(self.page_container, *services)

    def refresh_pages(self):
        # Rebuild dependent views so counts and reports reflect service updates.
        page_name = self.current_page
        if page_name in {"Dashboard", "Students", "Courses", "Enrollments", "Reports"}:
            self.show_page(page_name)
