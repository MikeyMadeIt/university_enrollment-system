
import tkinter as tk


class Header(tk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            bg="white",
            height=75
        )

        self.pack_propagate(False)

        self.build_header()

    def build_header(self):
        # Main branding container
        branding = tk.Frame(
            self,
            bg="white"
        )
        branding.pack(
            side="left",
            fill="y",
            padx=25
        )

        #Uni name and application name
        text_container = tk.Frame(
            branding,
            bg="white"
        )
        text_container.pack(
            side="left",
            fill="y"
        )

        university_name = tk.Label(
            text_container,
            text="QUEZON CITY UNIVERSITY",
            font=("Arial", 15, "bold"),
            fg="#07549C",
            bg="white"
        )
        university_name.pack(
            anchor="w",
            pady=(15, 0)
        )

        application_name = tk.Label(
            text_container,
            text="UNIVERSITY ENROLLMENT AND COURSE REGISTRATION SYSTEM",
            font=("Arial", 8),
            fg="#555555",
            bg="white"
        )
        application_name.pack(
            anchor="w"
        )

        #redunderline
        accent = tk.Frame(
            self,
            bg="#E30613",
            height=4
        )
        accent.place(
            relx=0,
            rely=1,
            relwidth=1,
            anchor="sw",
            height=4
        )
