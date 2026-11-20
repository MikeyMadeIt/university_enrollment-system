
import tkinter as tk

from .components.header import Header
from .components.sidebar import Sidebar
from .pages.dashboard import Dashboard
from .pages.students_page import StudentsPage
from .pages.courses_page import CoursesPage
from .pages.enrollments_page import EnrollmentsPage


class MainWindow:

    def __init__(self, root):
        self.root = root

        self.root.title("QCU - Course Registration System")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 650)

        self.root.configure(bg="#F1F3F5")

        self.build_layout()

    def build_layout(self):

        # Header
        self.header = Header(self.root)
        self.header.pack(fill="x")

        # Main body
        self.body = tk.Frame(
            self.root,
            bg="#F1F3F5"
        )
        self.body.pack(
            fill="both",
            expand=True
        )

        # Sidebar
        self.sidebar = Sidebar(
            self.body,
            self.show_page
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # Page container
        self.page_container = tk.Frame(
            self.body,
            bg="#F1F3F5"
        )
        self.page_container.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Default page
        self.sidebar.set_active("Dashboard")
        self.show_page("Dashboard")

    def show_page(self, page_name):

        # Clear previous page
        for widget in self.page_container.winfo_children():
            widget.destroy()

        if page_name == "Dashboard":
            Dashboard(self.page_container)

        elif page_name == "Students":
            StudentsPage(self.page_container)

        elif page_name == "Courses":
            CoursesPage(self.page_container)

        elif page_name == "Enrollments":
            EnrollmentsPage(self.page_container)
