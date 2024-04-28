import tkinter as tk
from  tkinter import ttk
import sqlite3
from PIL import ImageTk, Image
import db_functions as db
class gui():
    def __init__(self,root):
        self.loginWindow = root
        self.login_Window()

    def login_Window(self):

        self.loginWindow.geometry('400x600')
        self.loginWindow.title('Profile')
        self.loginWindow.resizable(False, False)
        self.username_label = tk.Label(self.loginWindow, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.loginWindow)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_label = tk.Label(self.loginWindow, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.loginWindow)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        self.login_button = tk.Button(self.loginWindow, text="Login", command=self.authenticate)

        self.login_button.grid(row=2, columnspan=2, pady=10)
        self.loginWindow.mainloop()

        self.username_entry.destroy()

    def authenticate(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if db.authenticateUser(entered_username, entered_password):
            self.profile(entered_username)
        else:
            self.invalid = tk.Label(self.loginWindow, text="invalid username or password")
            self.invalid.grid(row=4, column=0, padx=5, pady=5)



    def profile(self,username):

        self.username_entry.destroy()
        self.username_label.destroy()
        self.password_entry.destroy()
        self.password_label.destroy()
        self.login_button.destroy()
        self.invalid.destroy()

        self.img = Image.open("download.jpeg")
        # Resize the image
        self.img = self.img.resize((100, 100))
        self.img = ImageTk.PhotoImage(self.img)
        # Create a label and add the image to it
        imglabel = tk.Label(self.loginWindow, image=self.img)
        imglabel.grid(row=0, column=0, sticky='nw')

        userlist = db.searchByUsername(username)

        # Create a label to display the name
        namelocation = tk.Label(self.loginWindow, text="Name:", font=("Comic Sans MS", 20), fg="brown")
        namelocation.place(x=120, y=5)
        namelabel = tk.Label(self.loginWindow, text=userlist[1], font=("Comic Sans MS", 15), fg="black")
        namelabel.place(x=130, y=45)

