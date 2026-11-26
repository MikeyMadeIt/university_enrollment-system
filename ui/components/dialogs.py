"""Shared modal prompts used by the Tkinter pages."""

from tkinter import messagebox


def show_error(parent, title, error):
    messagebox.showerror(title, str(error), parent=parent)


def confirm(parent, title, message):
    return messagebox.askyesno(title, message, parent=parent)
