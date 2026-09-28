import tkinter as tk
from tkinter import messagebox
from config import APP_TITLE, ADMIN_USERNAME, ADMIN_PASSWORD
from gui.dashboard import Dashboard

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("430x320")
        self.resizable(False, False)

        tk.Label(self, text="CampusDesk", font=("Arial", 26, "bold")).pack(pady=(35, 5))
        tk.Label(self, text="Student Academic Management System").pack(pady=(0, 25))

        frame = tk.Frame(self)
        frame.pack()

        tk.Label(frame, text="Username").grid(row=0, column=0, padx=10, pady=8)
        self.username = tk.Entry(frame, width=25)
        self.username.grid(row=0, column=1)

        tk.Label(frame, text="Password").grid(row=1, column=0, padx=10, pady=8)
        self.password = tk.Entry(frame, width=25, show="*")
        self.password.grid(row=1, column=1)

        tk.Button(self, text="Login", width=18, command=self.login).pack(pady=20)
        tk.Label(self, text="Demo: admin / admin123", fg="gray").pack()

    def login(self):
        if self.username.get() == ADMIN_USERNAME and self.password.get() == ADMIN_PASSWORD:
            self.destroy()
            Dashboard().mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
