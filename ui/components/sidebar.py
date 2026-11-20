import tkinter as tk


class Sidebar(tk.Frame):

    PAGES = [
        "Dashboard",
        "Students",
        "Courses",
        "Enrollments",
        "Reports"
    ]

    def __init__(self, parent, on_navigate):
        super().__init__(
            parent,
            bg="#07549C",
            width=220
        )

        self.pack_propagate(False)

        self.on_navigate = on_navigate
        self.buttons = {}

        self.build_sidebar()

    def build_sidebar(self):

        heading = tk.Label(
            self,
            text="MAIN MENU",
            font=("Arial", 9, "bold"),
            fg="#DCEAF7",
            bg="#07549C",
            anchor="w"
        )

        heading.pack(
            fill="x",
            padx=18,
            pady=(25, 12)
        )

        self.create_navigation_buttons()

    def create_navigation_buttons(self):

        for page in self.PAGES:

            button = tk.Button(
                self,
                text=page,
                font=("Arial", 10),
                fg="white",
                bg="#07549C",
                activebackground="#FF6800",
                activeforeground="white",
                relief="flat",
                bd=0,
                anchor="w",
                padx=18,
                pady=11,
                cursor="hand2",
                command=lambda p=page: self.select_page(p)
            )

            button.pack(
                fill="x",
                padx=10,
                pady=2
            )

            self.buttons[page] = button

    def select_page(self, page):

        self.set_active(page)

        self.on_navigate(page)

    def set_active(self, selected_page):

        for page, button in self.buttons.items():

            if page == selected_page:
                button.configure(
                    bg="#FF6800",
                    font=("Arial", 10, "bold")
                )

            else:
                button.configure(
                    bg="#07549C",
                    font=("Arial", 10)
                )