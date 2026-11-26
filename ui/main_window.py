
import tkinter as tk

from .pages.records_page import RecordsPage
from .components.header import Header
from .components.sidebar import Sidebar
from .pages.dashboard import Dashboard
from .pages.students_page import StudentsPage
from .pages.courses_page import CoursesPage
from .pages.enrollments_page import EnrollmentsPage


class MainWindow:

    def __init__(self, root, student_service, course_service, enrollment_service,
                 report_service=None):
        self.root = root
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service
        self.report_service = report_service

        self.root.title("QCU - Course Registration System")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 650)

        self.root.configure(bg="#F1F3F5")

        self.build_layout()

    def build_layout(self):

        #header
        self.header = Header(self.root)
        self.header.pack(fill="x")

        self.body = tk.Frame(
            self.root,
            bg="#F1F3F5"
        )
        self.body.pack(
            fill="both",
            expand=True
        )

        #sidebar
        self.sidebar = Sidebar(
            self.body,
            self.show_page
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.page_container = tk.Frame(
            self.body,
            bg="#F1F3F5"
        )
        self.page_container.pack(
            side="left",
            fill="both",
            expand=True
        )

        #Default page
        self.sidebar.set_active("Dashboard")
        self.show_page("Dashboard")

    def show_page(self, page_name):
        self.current_page = page_name

        # Clear previous page
        for widget in self.page_container.winfo_children():
            widget.destroy()

        if page_name == "Dashboard":
            Dashboard(self.page_container, self.student_service, self.course_service,
                      self.enrollment_service)

        elif page_name == "Students":
            StudentsPage(self.page_container, self.student_service,
                         self.enrollment_service, self.course_service,
                         on_change=self.refresh_current_page)

        elif page_name == "Courses":
            CoursesPage(self.page_container, self.course_service,
                        self.enrollment_service, self.student_service,
                        on_change=self.refresh_current_page)

        elif page_name == "Enrollments":
            EnrollmentsPage(self.page_container, self.student_service,
                            self.course_service, self.enrollment_service,
                            on_change=self.refresh_current_page)

        elif page_name == "Records":
            RecordsPage(self.page_container, self.enrollment_service,
                        self.student_service, self.course_service,
                        on_change=self.refresh_current_page)

    def refresh_current_page(self):
        """Refresh the original page layout after a service operation."""
        current = getattr(self, "current_page", "Dashboard")
        self.show_page(current)
