import tkinter as tk
import ttkbootstrap as tkk
import sqlite3
from PIL import ImageTk, Image
import db_functions as db
# from tkinter import ttk


class Application(tk.Frame):
    def __init__(self, image,master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets(image)

    def create_widgets(self, image):
        self.gif = tkk.PhotoImage(file=image)
        self.label = tkk.Label(self, image=self.gif)
        self.label.pack()
        self.update_gif(0)

    def update_gif(self, frame):

        self.gif.configure(format="gif -index %i" % (frame % 25))
        self.after(50, self.update_gif, frame+1)


class gui():
    def __init__(self, root):
        self.loginWindow = root
        self.login_Window()

    flag = False
    def login_Window(self):

        if (self.flag):
            self.app.destroy()
            self.frame.destroy()
            self.username_entry.destroy()
            self.username_label.destroy()
            self.password_entry.destroy()
            self.password_label.destroy()
            self.login_button.destroy()
            self.invalid.destroy()
            self.createuser.destroy()
            self.newname_label.destroy()
            self.newname_entry.destroy()
            self.duplicate.destroy()
            self.signup_button.destroy()
            self.success.destroy()
            self.tologin_button.destroy()
        self.flag=True
        self.loginWindow.geometry('700x900')
        self.loginWindow.title('Profile')
        self.loginWindow.resizable(False, False)

        self.app = Application("topbar.gif",master=self.loginWindow)
        self.app.pack()

        # Then create a frame for the labels and entries
        self.frame = tk.Frame(self.loginWindow)
        self.frame.pack(expand=True)

        self.username_label = tkk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tkk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tkk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tkk.Entry(self.frame)
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tkk.Button(self.frame, text="Login", command=self.authenticate)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=0)
        self.loginWindow.bind("<Return>", lambda event: self.authenticate())

        self.createuser = tkk.Button(self.frame, text="Create new user")
        self.createuser.grid(row=4, column=0, columnspan=2, pady=5)
        self.createuser.bind("<Button-1>", lambda event: self.create_account())

        self.invalid = tkk.Label(self.frame, text="", foreground="red")
        self.invalid.grid(row=2, column=0, columnspan=2, pady=5)

        self.loginWindow.mainloop()
        self.frame.destroy()
        self.username_entry.destroy()

    def authenticate(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if db.authenticateUser(entered_username, entered_password):
            if db.isAdmin(entered_username):
                self.admin(entered_username)
                return 0
            self.profile(entered_username)
        else:
            self.invalid.config(text="Invalid username or password")

    def create_account(self):
        self.app.destroy()
        self.frame.destroy()
        self.username_entry.destroy()
        self.username_label.destroy()
        self.password_entry.destroy()
        self.password_label.destroy()
        self.login_button.destroy()
        self.invalid.destroy()
        self.createuser.destroy()

        self.app = Application("topbar.gif", master=self.loginWindow)
        self.app.pack()

        self.frame = tkk.Frame(self.loginWindow)
        self.frame.pack(expand=True)

        self.newname_label = tkk.Label(self.frame, text="Full name:")
        self.newname_label.grid(row=0, column=0, padx=5, pady=5)
        self.newname_entry = tkk.Entry(self.frame)
        self.newname_entry.grid(row=0, column=1, padx=5, pady=5)

        self.username_label = tkk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = tkk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        self.password_label = tkk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tkk.Entry(self.frame)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        self.signup_button = tkk.Button(self.frame, text="Sign Up",command=lambda: self.check_username(self.username_entry, self.password_entry,self.newname_entry), width=7)
        self.signup_button.grid(row=3, column=0, columnspan=1,padx= 5, pady=10)
        self.loginWindow.bind("<Return>", lambda event: self.check_username(self.username_entry, self.password_entry,self.newname_entry))
        self.duplicate = tkk.Label(self.frame, text="", foreground="red")
        self.duplicate.grid(row=4, column=0, columnspan=3, pady=5)
        self.success = tkk.Label(self.frame, text="", foreground="green")
        self.success.grid(row=5, columnspan=2, pady=5, column=0)
        self.tologin_button = tkk.Button(self.frame, text="Login", command=lambda: self.login_Window(), width=7)
        self.tologin_button.grid(row=3, column=1, columnspan=1,padx= 5, pady=10,)

    def check_username(self, username, password, name):
        username = username.get().strip()
        password = password.get().strip()
        name = name.get().strip()
        if (db.checkUserduplicates(username)):
            if(db.add_user(username, password, name)):
                self.newname_entry.delete(0, tkk.END)
                self.username_entry.delete(0, tkk.END)
                self.password_entry.delete(0, tkk.END)
                self.success.config(text="User Has Been Created Successfully")
            else:
                self.duplicate.config(text="You Have To Fulfill All The Fields")
        else:
            self.duplicate.config(text="Not Available Username")
    def profile(self,username):
        self.app.destroy()
        self.frame.destroy()
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
        imglabel = tkk.Label(self.loginWindow, image=self.img)
        imglabel.grid(row=0, column=0, sticky='nw')

        userlist = db.searchByUsername(username)

        # Create a label to display the name
        namelocation = tkk.Label(self.loginWindow, text="Name:", font=("Comic Sans MS", 20), foreground="brown")
        namelocation.place(x=120, y=5)
        namelabel = tkk.Label(self.loginWindow, text=userlist[1], font=("Comic Sans MS", 15), foreground="black")
        namelabel.place(x=130, y=45)

        ownedbookslabel = tkk.Label(self.loginWindow, text="Owned Books", font=("Comic Sans MS", 20),
                                    foreground="black", background="cyan")
        ownedbookslabel.place(relx=0.5, rely=0.16, anchor='center')

        booklist = db.get_books()  # This should return a list of tuples with book info

        for i, book in enumerate(booklist):
            book_name, book_cover, book_quantity = book

            # Calculate the row and column based on the index
            row = i // 2  # Integer division gives the row number
            col = i % 2  # Remainder gives the column number

            # Create a label to display the book name
            book_label = tk.Label(self.loginWindow, text=book_name, font=("Comic Sans MS", 15), fg="black",
                                  wraplength=100)
            book_label.place(x=200 + col * 170 * 2,
                             y=230 + row * 210)  # Adjust the x and y coordinates based on the row and column

            # Open, resize, and display the book cover
            img = Image.open(book_cover)
            img = img.resize((150, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.loginWindow, image=img)
            img_label.image = img  # Keep a reference to the image
            img_label.place(x=10 + col * 170 * 2,
                            y=180 + row * 210)  # Adjust the x and y coordinates based on the row and column

            # Create a label to display the book quantity
            # quantity_label = tk.Label(self.loginWindow, text=str(book_quantity), font=("Comic Sans MS", 15), fg="black")
            # quantity_label.place(x=280, y=85 + i * 60)

    def admin(self,username):
        self.app.destroy()
        self.frame.destroy()
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
        imglabel = tkk.Label(self.loginWindow, image=self.img)
        imglabel.grid(row=0, column=0, sticky='nw')

        userlist = db.searchByUsername(username)

        # Create a label to display the name
        namelocation = tkk.Label(self.loginWindow, text="admin:", font=("Comic Sans MS", 20), foreground="brown")
        namelocation.place(x=120, y=5)
        namelabel = tkk.Label(self.loginWindow, text=userlist[1], font=("Comic Sans MS", 15), foreground="black")
        namelabel.place(x=130, y=45)

        ownedbookslabel = tkk.Label(self.loginWindow, text="Owned Books", font=("Comic Sans MS", 20),
                                    foreground="black", background="cyan")
        ownedbookslabel.place(relx=0.5, rely=0.16, anchor='center')

        booklist = db.get_books()  # This should return a list of tuples with book info

        for i, book in enumerate(booklist):
            book_name, book_cover, book_quantity = book

            # Calculate the row and column based on the index
            row = i // 2  # Integer division gives the row number
            col = i % 2  # Remainder gives the column number

            # Create a label to display the book name
            book_label = tk.Label(self.loginWindow, text=book_name, font=("Comic Sans MS", 15), fg="black",
                                  wraplength=100)
            book_label.place(x=200 + col * 170 * 2,
                             y=230 + row * 210)  # Adjust the x and y coordinates based on the row and column

            # Open, resize, and display the book cover
            img = Image.open(book_cover)
            img = img.resize((150, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.loginWindow, image=img)
            img_label.image = img  # Keep a reference to the image
            img_label.place(x=10 + col * 170 * 2,
                            y=180 + row * 210)  # Adjust the x and y coordinates based on the row and column

            # Create a label to display the book quantity
            # quantity_label = tk.Label(self.loginWindow, text=str(book_quantity), font=("Comic Sans MS", 15), fg="black")
            # quantity_label.place(x=280, y=85 + i * 60)
