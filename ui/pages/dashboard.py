import tkinter as tk


class Dashboard:

    def __init__(self, parent, student_service, course_service, enrollment_service):
        self.parent = parent
        self.student_service = student_service
        self.course_service = course_service
        self.enrollment_service = enrollment_service

        self.frame = tk.Frame(
            self.parent,
            bg="#F1F3F5"
        )

        self.frame.pack(fill="both", expand=True)
        self.create_header()

        self.stats_frame = tk.Frame(
            self.frame,
            bg="#F1F3F5"
        )

        self.stats_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        students_card = self.create_stat_card(
            "Total Students",
            str(len(self.student_service.all()))
        )

        courses_card = self.create_stat_card(
            "Total Courses",
            str(len(self.course_service.all()))
        )

        enrollments_card = self.create_stat_card(
            "Total Enrollments",
            str(len(self.enrollment_service.all()))
        )

        students_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        courses_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        enrollments_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.capacity_frame = tk.Frame(
            self.frame,
            bg="#FFFFFF",
            highlightbackground="#D9DDE2",
            highlightthickness=1
        )

        self.capacity_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        self.create_capacity_section()
        self.create_course_list()

    def create_header(self):
        title = tk.Label(
            self.frame,
            text="Dashboard",
            font=("Arial", 22, "bold"),
            bg="#F1F3F5",
            fg="#07549C"
        )

        title.pack(anchor="w", padx=25, pady=20)


    def create_stat_card(self, title, value):
        card = tk.Frame(
            self.stats_frame,
            bg="#FFFFFF",
            padx=20,
            pady=15,
            highlightbackground="#D9DDE2",
            highlightthickness=1
        )

        label = tk.Label(
            card,
            text=title,
            font=("Arial", 11),
            fg="#555555",
            bg="#FFFFFF"
        )
        label.pack(anchor="w")

        number = tk.Label(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            fg="#333333",
            bg="#FFFFFF"
        )
        number.pack(anchor="w", pady=(8, 0))

        return card

    def create_capacity_section(self):
        title = tk.Label(
            self.capacity_frame,
            text="Courses Approaching Capacity",
            font=("Arial", 14, "bold"),
            fg="#07549C",
            bg="#FFFFFF"
        )

        title.pack(anchor="w", padx=20, pady=15)

    def create_course_list(self):

        self.course_list_frame = tk.Frame(
            self.capacity_frame,
            bg="#FFFFFF"
        )

        self.course_list_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )
        courses = []
        for course in self.course_service.all():
            count = self.enrollment_service.count_for_course(course["course_code"])
            if course["capacity"] and count / course["capacity"] >= 0.8:
                courses.append((course["course_code"], course["title"],
                                f"{count}/{course['capacity']}"))

        headers = ["Course Code", "Course Name", "Enrollment"]

        for column, header in enumerate(headers):
            label = tk.Label(
                self.course_list_frame,
                text=header,
                font=("Arial", 10, "bold"),
                bg="#E8EDF2",
                fg="#333333",
                anchor="w",
                padx=10,
                pady=10
            )

            label.grid(row=1, column=column, sticky="ew")

        for row, course in enumerate(courses, start=2):

            for column, value in enumerate(course):
                label = tk.Label(
                    self.course_list_frame,
                    text=value,
                    font=("Arial", 10),
                    bg="#FFFFFF",
                    fg="#333333",
                    anchor="w",
                    padx=10,
                    pady=12
                )

                label.grid(row=row, column=column, sticky="ew")

        for column in range(3):
            self.course_list_frame.grid_columnconfigure(
                column,
                weight=1
            )
