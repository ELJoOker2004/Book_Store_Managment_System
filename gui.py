import tkinter as tk
import ttkbootstrap as tkk
import sqlite3
from PIL import ImageTk, Image
import db_functions as db
# from tkinter import ttk
import mainWindow as mw
import webbrowser
from tkinter import Canvas, Scrollbar , Frame

class Application(tk.Frame):
    def __init__(self, image,frames,speed,master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets(image,frames,speed)

    def create_widgets(self, image,frames,speed):
        self.gif = tkk.PhotoImage(file=image)
        self.label = tkk.Label(self, image=self.gif)
        self.label.pack()
        self.update_gif(0,frames,speed)

    def update_gif(self, frame,frames,speed):

        self.gif.configure(format="gif -index %i" % (frame % frames))
        self.after(speed, self.update_gif, frame+1,frames,speed)


class Gui():
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
        self.loginWindow.title('Login')
        self.loginWindow.resizable(False, False)

        self.app = Application("topbar.gif",25,50,master=self.loginWindow)
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
        self.password_entry = tkk.Entry(self.frame, show="•")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tkk.Button(self.frame, text="Login", command=self.authenticate,bootstyle="dark")
        self.login_button.grid(row=3, column=0, columnspan=2, pady=0)
        self.loginWindow.bind("<Return>", lambda event: self.authenticate())

        self.createuser = tkk.Button(self.frame, text="Create new user",bootstyle="dark-link")
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
            self.app.destroy()
            self.frame.destroy()
            self.username_entry.destroy()
            self.username_label.destroy()
            self.password_entry.destroy()
            self.password_label.destroy()
            self.login_button.destroy()
            self.invalid.destroy()
            self.createuser.destroy()
            self.mainWindow(entered_username)

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
        self.loginWindow.title('Create Account')
        self.app = Application("welcome-anime.gif",22,90, master=self.loginWindow)
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
        self.password_entry = tkk.Entry(self.frame, show="•")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        self.signup_button = tkk.Button(self.frame, text="Sign Up",command=lambda: self.check_username(self.username_entry, self.password_entry,self.newname_entry), width=7, bootstyle="success")
        self.signup_button.grid(row=3, column=0, columnspan=1,padx= 5, pady=10)
        self.loginWindow.bind("<Return>", lambda event: self.check_username(self.username_entry, self.password_entry,self.newname_entry))
        self.duplicate = tkk.Label(self.frame, text="", foreground="red")
        self.duplicate.grid(row=4, column=0, columnspan=3, pady=5)
        self.success = tkk.Label(self.frame, text="", foreground="green")
        self.success.grid(row=5, columnspan=2, pady=5, column=0)
        self.tologin_button = tkk.Button(self.frame, text="Login", command=lambda: self.login_Window(), width=7,bootstyle="dark")
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
        self.loginWindow.title('Profile')
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
                                  wraplength=120)
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
        self.createuser.destroy()

        self.loginWindow.title('Admin Page')
        self.img = Image.open("download.jpeg")
        # Resize the image
        self.img = self.img.resize((100, 100))
        self.img = ImageTk.PhotoImage(self.img)
        # Create a label and add the image to it
        imglabel = tkk.Label(self.loginWindow, image=self.img)
        imglabel.pack(anchor='nw')

        userlist = db.searchByUsername(username)

        # Create a label to display the name
        namelocation = tkk.Label(self.loginWindow, text="Admin:", font=("Comic Sans MS", 20), foreground="brown")
        namelocation.place(x=120, y=5)
        namelabel = tkk.Label(self.loginWindow, text=userlist[1], font=("Comic Sans MS", 15), foreground="black")
        namelabel.place(x=130, y=45)

        frame2 = Frame(self.loginWindow)
        frame2.pack(pady=20)
        # Create a new frame
        frame = Frame(self.loginWindow)
        frame.pack(fill='both', expand=True)  # Adjust the fill and expand options

        # Create a canvas and a vertical scrollbar
        canvas = Canvas(frame)
        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configure the canvas to be scrollable
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind the scroll wheel event to the yview_scroll method
        canvas.bind("<MouseWheel>",
                    lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))  # For Windows
        canvas.bind("<Button-4>", lambda event: canvas.yview_scroll(int(-1), "units"))  # For Linux
        canvas.bind("<Button-5>", lambda event: canvas.yview_scroll(int(1), "units"))  # For Linux

        # Place the canvas and the scrollbar in the frame
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        booklist = db.get_books()  # This should return a list of tuples with book info

        for i, book in enumerate(booklist):
            book_id,book_name, book_cover, book_quantity = book

            # Open, resize, and display the book cover
            img = Image.open(book_cover)
            img = img.resize((150, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(scrollable_frame, image=img)
            img_label.image = img  # Keep a reference to the image
            img_label.grid(row=i, column=1)

            # Create a label to display the book name
            book_label = tk.Label(scrollable_frame, text=book_name, font=("Comic Sans MS", 15), fg="black",
                                  wraplength=100)
            book_label.grid(row=i, column=0)

            # Create a label to display the book quantity
            quantity_label = tk.Label(scrollable_frame, text=str(book_quantity), font=("Comic Sans MS", 15), fg="black")
            quantity_label.grid(row=i, column=2)

            # Create + and - buttons
            plus_button = tk.Button(scrollable_frame, text="+",font=("Comic Sans MS",10), command=lambda b_id=book_id: [db.increase_book(b_id),quantity_label.config(text=str(book_quantity))])
            minus_button = tk.Button(scrollable_frame, text="-",font=("Comic Sans MS",10), command=lambda b_id=book_id: db.decrease_book(b_id))
            plus_button.grid(row=i, column=3,padx=1)
            minus_button.grid(row=i, column=4,padx=1)

        # Create a label, entry, and button on the right side of the page
        right_label = tk.Label(self.loginWindow, text="Right Label", font=("Comic Sans MS", 20), fg="black")
        right_label.pack(side="right")
        right_entry = tk.Entry(self.loginWindow)
        right_entry.pack(side="right")
        right_button = tk.Button(self.loginWindow, text="Right Button", command=lambda: print("Button clicked"))
        right_button.pack(side="right")
    def mainWindow(self,username):
        # frames
        self.loginWindow.title('Market')
        # Top frame
        topFrame = tk.Frame(self.loginWindow, width=1350, height=50, padx=10, relief="sunken", borderwidth=2)
        topFrame.pack()

        # center frame
        centerFrame = tk.Frame(self.loginWindow, width=1350, height=680, relief="ridge", bg="red")
        centerFrame.pack()

        # center left frame
        centerLeftFrame = tk.Frame(centerFrame, width=100, height=700, borderwidth=2, relief="sunken", bg="grey")
        centerLeftFrame.pack(side="left")

        # center right frame
        centerRightFrame = tk.Frame(centerFrame, width=1250, height=700, borderwidth=2, relief="sunken", bg="orange")
        centerRightFrame.pack()

        # search bar
        searchbar = tk.LabelFrame(centerRightFrame, width=1200, height=100, bg="white")
        searchbar.pack(fill="both")
        self.lbl_search = tk.Label(searchbar, text="Search", font="Times 12 bold", bg="grey", fg="white")
        self.lbl_search.grid(row=0, column=0)
        self.ent_search = tk.Entry(searchbar, width=1000)

        def on_entry_click(event):
            """Function to handle when the user clicks inside the entry."""

            if self.ent_search.get() == "Search Here":
                self.ent_search.delete(0, tk.END)  # Clear the placeholder text
                self.ent_search.config(fg='black')  # Change text color to black

        def on_focus_out(event):
            """Function to handle when the self.ent_search loses focus."""

            if self.ent_search.get() == "":
                self.ent_search.insert(0, "Search Here")  # Restore placeholder text
                self.ent_search.config(fg='grey')  # Change text color to grey

        def search():
            """Function to handle the search."""

            search_term = self.ent_search.get()
            print("Searching for:", search_term)

        self.ent_search.bind("<FocusIn>", on_entry_click)
        self.ent_search.bind("<FocusOut>", on_focus_out)
        # search button
        search_button = tk.Button(searchbar, text="Search", command=search, width=7, height=1)
        search_button.grid(row=0, column=0, padx=(3, 10), pady=5)

        # Perform search operation here
        self.ent_search.insert(0, "Search here")
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        # hyperlinks for the left side
        def open_link_1():
            topFrame.destroy()
            centerFrame.destroy()
            self.profile(username)

        def open_link_2():
            webbrowser.open("https://www.example2.com")

        def open_link_3():
            webbrowser.open("https://www.example3.com")

        def open_link_4():
            webbrowser.open("https://www.example4.com")

        links = [
            ("Profile", open_link_1),
            ("Settings", open_link_2),
            ("Contact us", open_link_3),
            ("About us", open_link_4),
            ("Help", open_link_1),
            ("Version", open_link_2)
        ]

        for text, command in links:
            label = tk.Label(centerLeftFrame, text=text, fg="black", cursor="arrow", bg="grey", width=10)
            label.pack(pady=5)
            label.bind("<Button-1>", lambda event, cmd=command: cmd())

            # Change cursor when hovering over the label
            label.bind("<Enter>", label.config(cursor="hand2"))
            label.bind("<Leave>", lambda event: label.config(cursor="arrow"))

        leftpanel = tk.Label(centerLeftFrame, bg="grey", width=10, height=700)
        leftpanel.pack()

        # header of the main page
        header = tk.Label(topFrame, text="WELCOME BACK", fg="black", width=1350)
        header.config(font=("Times New Roman", 48), pady=30)
        header.pack()

        # books = tk.LabelFrame(centerRightFrame, width= 1250, height=600, bg="green")
        # books.pack()
