
import tkinter as tk
from tkinter import messagebox, ttk

from ui.components.dialogs import AddCourseDialog, EnrolledStudentsDialog


class CoursesPage:

    def __init__(self, parent, course_service, enrollment_service,
                 student_service, on_change=None):
        self.parent = parent
        self.course_service = course_service
        self.enrollment_service = enrollment_service
        self.student_service = student_service
        self.on_change = on_change

        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )
        self.frame.pack(fill="both", expand=True)

        self.load_courses()
        self.load_students()

        self.create_header()
        self.create_search_bar()
        self.create_course_table()

    def create_header(self):

        title = tk.Label(
            self.frame,
            text="Courses",
            font=("Arial", 22, "bold"),
            bg="#F1F3F5",
            fg="#07549C"
        )
        title.pack(anchor="w", padx=25, pady=(25, 5))

        subtitle = tk.Label(
            self.frame,
            text="Manage available courses and course information",
            font=("Arial", 10),
            bg="#F1F3F5",
            fg="#555555"
        )
        subtitle.pack(anchor="w", padx=25)

    def create_search_bar(self):

        search_frame = tk.Frame(
            self.frame,
            bg="#F1F3F5"
        )
        search_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Search input
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8,
            padx=(0, 10)
        )

        self.search_entry.insert(
            0,
            "Search by course code"
        )
        self.search_entry.config(fg="#888888")
        self.search_entry.bind("<FocusIn>", self.clear_search_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_search_placeholder)

        # Search button
        search_button = tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.search_courses
        )
        search_button.pack(side="right")

    def create_course_table(self):

        # Table container
        table_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 10)
        )

        # Table title
        table_title = tk.Label(
            table_frame,
            text="Available Courses",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#07549C"
        )
        table_title.pack(
            anchor="w",
            padx=15,
            pady=15
        )

        columns = (
            "course_code",
            "course_name",
            "capacity",
            "enrolled"
        )

        self.course_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.course_tree.heading(
            "course_code",
            text="Course Code"
        )

        self.course_tree.heading(
            "course_name",
            text="Course Name"
        )

        self.course_tree.heading(
            "capacity",
            text="Capacity"
        )

        self.course_tree.heading(
            "enrolled",
            text="Enrolled"
        )

        self.course_tree.column(
            "course_code",
            width=130,
            anchor="center"
        )

        self.course_tree.column(
            "course_name",
            width=300,
            anchor="w"
        )

        self.course_tree.column(
            "capacity",
            width=120,
            anchor="center"
        )

        self.course_tree.column(
            "enrolled",
            width=120,
            anchor="center"
        )

        # Display course records loaded from the course and enrollment services.
        for course_code, details in self.courses.items():

            self.course_tree.insert(
                "",
                "end",
                iid=course_code,
                values=(
                    course_code,
                    details["name"],
                    details["capacity"],
                    len(details["enrolled"])
                )
            )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.course_tree.yview
        )

        self.course_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.course_tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0),
            pady=(0, 15)
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 15),
            pady=(0, 15)
        )

        # Double-click event
        self.course_tree.bind(
            "<Double-1>",
            self.open_enrolled_students
        )
        self.course_tree.bind(
            "<Delete>",
            lambda _event: self.delete_selected_course()
        )

        # Add Course button below the table
        add_button = tk.Button(
            self.frame,
            text="+ Add Course",
            font=("Arial", 10, "bold"),
            bg="#07549C",
            fg="#FFFFFF",
            activebackground="#06447D",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.open_add_course_dialog
        )

        add_button.pack(
            anchor="e",
            padx=25,
            pady=(0, 20)
        )

    def clear_search_placeholder(self, _event=None):
        if self.search_entry.get() == "Search by course code":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg="#333333")

    def restore_search_placeholder(self, _event=None):
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "Search by course code")
            self.search_entry.config(fg="#888888")

    def open_add_course_dialog(self):
        AddCourseDialog(self.frame, self.courses, self._add_course)

    def _add_course(self, code, title, capacity, prerequisites):
        self.course_service.add(code, title, capacity, prerequisites)
        self.load_courses()
        self.refresh_courses()
        if self.on_change:
            self.on_change()

    def search_courses(self):
        query = self.search_entry.get().strip()
        if query == "Search by course code":
            query = ""
        if not query:
            self.refresh_courses()
            return
        results = self.course_service.search(query)
        self.display_courses(results)

    def delete_selected_course(self):
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showwarning("No Course Selected", "Select a course to delete.",
                                   parent=self.frame.winfo_toplevel())
            return
        code = self.course_tree.item(selected[0], "values")[0]
        if self.course_service.has_dependents(code):
            messagebox.showerror("Course", f"{code} is a prerequisite for another course.",
                                 parent=self.frame.winfo_toplevel())
            return
        if not messagebox.askyesno("Confirm Deletion", f"Delete course {code} and its enrollments?",
                                   parent=self.frame.winfo_toplevel()):
            return
        try:
            self.enrollment_service.drop_all_for_course(code)
            self.course_service.remove(code)
            self.refresh_courses()
            if self.on_change:
                self.on_change()
        except (ValueError, OSError) as exc:
            messagebox.showerror("Delete Failed", str(exc), parent=self.frame.winfo_toplevel())

    def display_courses(self, courses):
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        for row in courses:
            code = row["course_code"]
            enrolled = self.enrollment_service.count_for_course(code)
            self.course_tree.insert("", "end", iid=code, values=(
                code, row["title"], row["capacity"], enrolled
            ))

    def refresh_courses(self):
        self.load_courses()
        self.display_courses(self.course_service.all())

    def open_enrolled_students(self, event=None):

        selected_item = self.course_tree.selection()

        if not selected_item:
            return

        course_code = self.course_tree.item(selected_item[0], "values")[0]
        course_details = self.course_service.get(course_code)
        records = self.enrollment_service.for_course(course_code)
        enrolled_ids = [row["student_id"] for row in records]
        EnrolledStudentsDialog(
            self.frame, course_code, course_details["title"], enrolled_ids,
            self.students, course_details.get("prerequisites", []), self.courses,
            self._drop_enrolled_student
        )

    def _drop_enrolled_student(self, student_id, course_code):
        self.enrollment_service.drop(student_id, course_code)
        self.refresh_courses()
        if self.on_change:
            self.on_change()

    def load_courses(self):
        self.courses = {}
        for course in self.course_service.all():
            code = course["course_code"]
            self.courses[code] = {
                "name": course["title"], "capacity": course["capacity"],
                "enrolled": {row["student_id"] for row in self.enrollment_service.for_course(code)},
                "prerequisites": set(course.get("prerequisites", [])),
            }

    def load_students(self):
        self.students = {row["student_id"]: row for row in self.student_service.all()}


# Testing
# if __name__ == "__main__":
#
#     root = tk.Tk()
#     root.title("QCU Enrollment System")
#     root.geometry("1000x650")
#
#     CoursesPage(root)
#
#     root.mainloop()
