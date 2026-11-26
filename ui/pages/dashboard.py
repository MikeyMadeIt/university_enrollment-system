from tkinter import ttk


class Dashboard:
    def __init__(self, parent, student_service, course_service, enrollment_service):
        frame = ttk.Frame(parent, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="University Enrollment System", font=("Arial", 22, "bold")).pack(anchor="w", pady=(0, 20))
        for title, count in (("Students", len(student_service.all())),
                             ("Courses", len(course_service.all())),
                             ("Current enrollments", len(enrollment_service.all()))):
            card = ttk.LabelFrame(frame, text=title, padding=18)
            card.pack(fill="x", pady=7)
            ttk.Label(card, text=str(count), font=("Arial", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Use the navigation menu to manage enrollment records.").pack(anchor="w", pady=12)
