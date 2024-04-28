import tkinter as tk
import ttkbootstrap as tkk
from PIL import ImageTk, Image


def authenticate(self):
    entered_username = self.username_entry.get()
    entered_password = self.password_entry.get()

    if db.authenticateUser(entered_username, entered_password):
        self.profile(entered_username)
    else:
        self.invalid.config(text="Invalid username or password")


root = tkk.Window()
root.title('Book Store Manager')
root.geometry('400x600')
root.resizable(False, False)

frame = tkk.Frame(master=root)
frame.pack(expand=True)

username_label = tkk.Label(master=frame, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tkk.Entry(master=frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = tkk.Label(master=frame, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tkk.Entry(master=frame)
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tkk.Button(frame, text="Login", command=authenticate)
login_button.grid(row=3, column=0, columnspan=2, pady=0)
root.bind("<Return>", lambda event: authenticate)

invalid = tkk.Label(frame, text="", foreground="red")
invalid.grid(row=2, column=0, columnspan=2, pady=5)

root.mainloop()
frame.destroy()

