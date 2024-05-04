import tkinter as tk
import ttkbootstrap as tkk
import sqlite3
from PIL import ImageTk, Image
import db_functions as db
# from tkinter import ttk
import mainWindow as mw
import webbrowser
from tkinter import Canvas, Scrollbar , Frame
import destroy as ds

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
        self.cart = []
        self.login_Window()

    def open_new_window(self,username):
        # Create a new window
        new_window = tk.Toplevel(self.loginWindow)
        new_window.title('Remove Book Panel')

        # Create a label for the dropdown menu
        label = tk.Label(new_window, text="Select ID", font=("Comic Sans MS", 12))
        label.pack(side="left", padx=(10, 10))

        # Get the list of books
        booklist = db.get_books()  # This should return a list of tuples with book info

        # Extract the book IDs into a list
        book_ids = [book[0] for book in booklist]

        # Create a StringVar for the dropdown menu
        id_var = tk.StringVar(new_window)
        id_var.set(book_ids[0])  # Set the default option

        # Create a dropdown menu with the book IDs
        dropdown = tkk.Combobox(new_window, textvariable=id_var, values=book_ids)
        dropdown.pack(side="left")

        confirm = tk.Button(new_window, text="Confirm", font=("Comic Sans MS", 12),foreground="blue", command= lambda:[db.delete_book(id_var.get()),self.admin(username),new_window.destroy(),self.open_new_window(username)])
        confirm.pack(side="left")

    def open_members_window(self,ogusername):
        # Create a new window
        new_window = tk.Toplevel(self.loginWindow)
        new_window.title('Members')

        # Get the list of members
        members = db.show_members()
        role_vars = {}
        username_label = tkk.Label(new_window, text="username", font=("Comic Sans MS", 12))
        username_label.grid(row=0, column=0)
        username_label = tkk.Label(new_window, text="Name", font=("Comic Sans MS", 12))
        username_label.grid(row=0, column=1)
        username_label = tkk.Label(new_window, text="Books Owned",font=("Comic Sans MS", 12))
        username_label.grid(row=0, column=2)
        username_label = tkk.Label(new_window, text="Role",font=("Comic Sans MS", 12))
        username_label.grid(row=0, column=3)
        for i, member in enumerate(members):
            username, name, books_owned, role = member

            username_label = tkk.Label(new_window, text=username,font=("Comic Sans MS", 10))
            username_label.grid(row=i + 1, column=0)

            name_label = tkk.Label(new_window, text=name,font=("Comic Sans MS", 10))
            name_label.grid(row=i + 1, column=1)

            # Check if books_owned is not None
            if books_owned is not None:
                books_owned_text = ''.join(books_owned)
            else:
                books_owned_text = ''

            books_owned_label = tkk.Label(new_window, text=books_owned_text,font=("Comic Sans MS", 10))
            books_owned_label.grid(row=i + 1, column=2)

            # Create a dropdown menu for the role
            role_var = tkk.StringVar(new_window)
            role_dropdown = tkk.Combobox(new_window, textvariable=role_var, values=['admin', 'member'])
            role_dropdown.grid(row=i + 1, column=3)
            role_var.set(role)  # Set the default option after creating the Combobox

            role_vars[username] = role_var  # Store the StringVar in the dictionary

        def confirm_roles():
            for username, role_var in role_vars.items():
                db.change_role(role_var.get(), username)

        confirm = tk.Button(new_window, text="Confirm", font=("Comic Sans MS", 12), foreground="blue",
                            command=lambda:[confirm_roles(),new_window.destroy(),self.admin(ogusername)])  # Update the command
        confirm.grid(columnspan=4,column=0)

    def add_book_window(self,username):
        # Create a new window
        new_window = tk.Toplevel(self.loginWindow)
        new_window.title('Add Book')

        # Create labels and entry fields for book details
        name_label = tkk.Label(new_window, text="Book Name", font=("Comic Sans MS", 12))
        name_label.grid(row=0, column=0)
        name_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        name_entry.grid(row=0, column=1)

        cover_label = tkk.Label(new_window, text="Cover Path (prefer relative path to the app directory)", font=("Comic Sans MS", 12))
        cover_label.grid(row=1, column=0)
        cover_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        cover_entry.grid(row=1, column=1)

        quantity_label = tkk.Label(new_window, text="Quantity (Positive Number)", font=("Comic Sans MS", 12))
        quantity_label.grid(row=2, column=0)
        quantity_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        quantity_entry.grid(row=2, column=1)

        author_label = tkk.Label(new_window, text="Author", font=("Comic Sans MS", 12))
        author_label.grid(row=3, column=0)
        author_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        author_entry.grid(row=3, column=1)

        description_label = tkk.Label(new_window, text="Description", font=("Comic Sans MS", 12))
        description_label.grid(row=4, column=0)
        description_entry = tkk.Text(new_window, font=("Comic Sans MS", 10), width=50, height=7)
        description_entry.grid(row=4, column=1,pady=1)

        # Function to add the book to the database
        def add_book_to_db():
            name = name_entry.get()
            cover = cover_entry.get()
            quantity = quantity_entry.get()
            author = author_entry.get()
            description = description_entry.get("1.0", "end").strip()
            db.add_book(name, cover, quantity,author,description)

        # Create an 'Add Book' button
        add_button = tk.Button(new_window, text="Add Book", font=("Comic Sans MS", 12), foreground="blue",
                               command=lambda:[add_book_to_db(),new_window.destroy(),self.admin(username)])
        add_button.grid(row=5, column=0, columnspan=2)

    def edit_book_window(self, username, book_id, book_name, book_cover, book_quantity, author,description):
        # Create a new window
        new_window = tk.Toplevel(self.loginWindow)
        new_window.title('Edit Book')

        # Create labels and entry fields for book details
        # Pre-fill the entry fields with the current details of the book
        name_label = tkk.Label(new_window, text="Book Name", font=("Comic Sans MS", 12))
        name_label.grid(row=0, column=0)
        name_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        name_entry.insert(0, book_name)
        name_entry.grid(row=0, column=1)

        cover_label = tkk.Label(new_window, text="Cover Path (prefer relative path to the app directory)",
                                font=("Comic Sans MS", 12))
        cover_label.grid(row=1, column=0)
        cover_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        cover_entry.insert(0, book_cover)
        cover_entry.grid(row=1, column=1)

        quantity_label = tkk.Label(new_window, text="Quantity (Positive Number)", font=("Comic Sans MS", 12))
        quantity_label.grid(row=2, column=0)
        quantity_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        quantity_entry.insert(0, book_quantity)
        quantity_entry.grid(row=2, column=1)

        author_label = tkk.Label(new_window, text="Author", font=("Comic Sans MS", 12))
        author_label.grid(row=3, column=0)
        author_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        author_entry.insert(0, author)
        author_entry.grid(row=3, column=1)

        description_label = tkk.Label(new_window, text="Description", font=("Comic Sans MS", 12))
        description_label.grid(row=4, column=0)
        description_entry = tkk.Text(new_window, font=("Comic Sans MS", 10), width=50, height=7)
        description_entry.insert('1.0', description)
        description_entry.grid(row=4, column=1,pady=10)
        # Function to update the book in the database
        def update_book_in_db():
            new_name = name_entry.get()
            new_cover = cover_entry.get()
            new_quantity = quantity_entry.get()
            new_author = author_entry.get()
            new_description = description_entry.get("1.0", "end").strip()
            db.edit_book(book_id, new_name, new_cover, int(new_quantity), new_author,new_description)

        # Create an 'Edit Book' button
        edit_button = tk.Button(new_window, text="Edit Book", font=("Comic Sans MS", 12), foreground="blue",
                                command=lambda: [update_book_in_db(), new_window.destroy(), self.admin(username)])
        edit_button.grid(row=5, column=0, columnspan=2)

    def login_Window(self):
        ds.destruction(self)
        self.loginWindow.geometry('800x900')
        self.loginWindow.title('Login')
        self.loginWindow.resizable(False, False)

        self.app = Application("resources/topbar.gif",25,50,master=self.loginWindow)
        self.app.pack()
        self.loginWindow.bind("<MouseWheel>",
                              lambda event: None)
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
        try:
            self.unauthorized.destroy()
        except:
            pass
        ds.destruction(self)
        self.loginWindow.title('Create Account')
        self.app = Application("resources/welcome-anime.gif",22,90, master=self.loginWindow)
        self.app.pack()

        self.frame = tkk.Frame(self.loginWindow)
        self.frame.pack(expand=True)
        self.loginWindow.bind("<MouseWheel>",
                              lambda event: None)
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

    def profile(self, username):
        ds.destruction(self)
        folder = "images\\"
        self.loginWindow.title('Profile')
        self.img = Image.open("resources/download.jpeg")
        # Resize the image
        self.img = self.img.resize((100, 100))
        self.img = ImageTk.PhotoImage(self.img)
        # Create a label and add the image to it
        self.imglabel = tkk.Label(self.loginWindow, image=self.img)
        self.imglabel.pack(anchor='nw')
        # Open the sign out icon image
        self.signout_img = Image.open("resources/leaving.png")
        self.signout_img = self.signout_img.resize((70, 70))  # Resize the image
        self.signout_img = ImageTk.PhotoImage(self.signout_img)

        # Create a button with the sign out icon
        self.signout_button = tk.Button(self.loginWindow, image=self.signout_img, command=lambda: self.login_Window(),
                                        highlightthickness=0, bd=0)
        self.signout_button.image = self.signout_img
        # Place the sign out button at the top right of the window
        self.signout_button.place(relx=1, rely=0, anchor='ne')
        self.market_img = Image.open("resources/market.jpeg")
        self.market_img = self.market_img.resize((70, 70))  # Resize the image
        self.market_img = ImageTk.PhotoImage(self.market_img)

        # Create a button with the sign out icon
        self.market_button = tk.Button(self.loginWindow, image=self.market_img, command=lambda: self.mainWindow(username),
                                        highlightthickness=0, bd=0)
        self.market_button.image = self.market_img
        # Place the sign out button at the top right of the window
        self.market_button.place(x=660,y=0)

        userlist = db.searchByUsername(username)

        # Create a label to display the name
        self.namelocation = tkk.Label(self.loginWindow, text="Name:", font=("Comic Sans MS", 20), foreground="brown")
        self.namelocation.place(x=120, y=5)
        self.namelabel = tkk.Label(self.loginWindow, text=userlist[1], font=("Comic Sans MS", 15), foreground="black")
        self.namelabel.place(x=130, y=45)
        self.centerFrame = tk.Frame(self.loginWindow, width=1250, height=15, borderwidth=2)
        self.centerFrame.pack()
        self.ownedbookslabel = tkk.Label(self.loginWindow, text="Owned Books", font=("Comic Sans MS", 20),
                                         foreground="black", background="cyan", anchor="center", justify="center")
        self.ownedbookslabel.pack(fill="both")

        self.frame2 = Frame(self.loginWindow)
        self.frame2.pack(pady=10)
        # Create a new frame
        self.frame = Frame(self.loginWindow)
        self.frame.pack(fill='both', expand=True)  # Adjust the fill and expand options

        # Create a canvas and a vertical scrollbar
        self.canvas = Canvas(self.frame)
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Bind the scroll wheel event to the yview_scroll method
        self.loginWindow.bind("<MouseWheel>",
                         lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))  # For Windows
        # self.loginWindow.bind("<Button-4>", lambda event: self.canvas.yview_scroll(int(-1), "units"))  # For Linux
        # self.loginWindow.bind("<Button-5>", lambda event: self.canvas.yview_scroll(int(1), "units"))  # For Linux

        # Configure the canvas to be scrollable
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        # Create a frame inside the canvas to hold the images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")

        # Add images to the image frame
        self.images = []

        self.added_labels = {}
        booklist = db.get_user_books(username)
        for s, book in enumerate(booklist):
            book_id, book_name, book_cover, book_quantity, author,description = book

            img = Image.open(folder + book_cover)
            img = img.resize((130, 200))
            tk_img = ImageTk.PhotoImage(img)
            row = s // 2  # Integer division - each row will contain 2 books
            col = s % 2 * 2  # Each book
            self.images.append(tk_img)
            self.label = tk.Label(self.image_frame, image=tk_img)
            self.label.grid(row=row, column=col, pady=10)

            self.txt = tk.Frame(self.image_frame)
            self.txt.grid(row=row, column=col + 1, padx=63)
            # book name
            self.bookName = tk.Label(self.txt, text=book_name, font=("Times New Roman", 15), wraplength=140)
            self.bookName.grid(row=0, column=0, pady=0)
            # hyperlinks of books names
            self.bookName.bind("<Button-1>",
                               lambda event, command=lambda: self.reading(): command())
            self.bookName.bind("<Enter>", self.bookName.config(cursor="hand2", fg="blue"))
            self.bookName.bind("<Leave>", lambda event: self.bookName.config(cursor="arrow", fg="black"))

            # author name
            self.bookAuthor = tk.Label(self.txt, text=f"By: {author}", font=("Times New Roman italic", 12), anchor="sw")
            self.bookAuthor.grid(row=1, column=0)

            self.bookDetails = tk.Button(self.txt, text="Book Details", width=12, height=1,
                                         command=lambda b_cover=book_cover, a_id = book_id, usernamet = username: self.bookInfo((folder +b_cover),book_name,author,a_id,usernamet,True))
            self.bookDetails.grid(row=2, column=0, pady=10)

        # Update the canvas scroll region
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def admin(self,username):
        ds.destruction(self)

        self.app.destroy()
        self.frame.destroy()
        try:
            self.unauthorized.destroy()
        except:
            pass
        self.username_entry.destroy()
        self.username_label.destroy()
        self.password_entry.destroy()
        self.password_label.destroy()
        self.login_button.destroy()
        self.invalid.destroy()
        self.createuser.destroy()
        if db.isAdmin(username):
            pass
        else:
            self.unauthorized = tkk.Label(self.loginWindow, text="Unauthorized Access",foreground="red",font=(50))
            self.unauthorized.pack(fill="both",side="bottom",padx=320)
            self.login_Window()
        self.loginWindow.title('Admin Page')
        self.img = Image.open("resources/download.jpeg")
        # Resize the image
        self.img = self.img.resize((100, 100))
        self.img = ImageTk.PhotoImage(self.img)
        # Create a label and add the image to it
        self.imglabel = tkk.Label(self.loginWindow, image=self.img)
        self.imglabel.pack(anchor='nw')
        # Open the sign out icon image
        self.signout_img = Image.open("resources/leaving.png")
        self.signout_img = self.signout_img.resize((70, 70))  # Resize the image
        self.signout_img = ImageTk.PhotoImage(self.signout_img)

        # Create a button with the sign out icon
        self.signout_button = tk.Button(self.loginWindow, image=self.signout_img, command=lambda: self.login_Window(), highlightthickness=0, bd=0)
        self.signout_button.image = self.signout_img
        # Place the sign out button at the top right of the window
        self.signout_button.place(relx=1, rely=0, anchor='ne')

        userlist = db.searchByUsername(username)

        # Create a label to display the name
        self.namelocation = tkk.Label(self.loginWindow, text="Admin:", font=("Comic Sans MS", 20), foreground="brown")
        self.namelocation.place(x=120, y=5)
        self.namelabel = tkk.Label(self.loginWindow, text=userlist[1], font=("Comic Sans MS", 15), foreground="black")
        self.namelabel.place(x=130, y=45)
        self.manage_members_button = tk.Button(self.loginWindow, text="Manage Members", font=("Comic Sans MS", 12),foreground="blue", command=lambda: self.open_members_window(username))
        self.manage_members_button.place(x=5, y=115)
        self.add_book_button = tk.Button(self.loginWindow, text="Add New Book",font=("Comic Sans MS", 12),foreground="blue", command=lambda: self.add_book_window(username))
        self.add_book_button.place(x=150, y=115)

        self.remove_book_button = tk.Button(self.loginWindow, text="Remove Book", font=("Comic Sans MS", 12),foreground="blue", command=lambda:self.open_new_window(username))
        self.remove_book_button.place(x=270, y=115)
        self.refresh_button = tk.Button(self.loginWindow, text="Refresh", font=("Comic Sans MS", 12), foreground="blue",command=lambda: self.admin(username))
        self.refresh_button.place(x=725, y=115)
        self.centerFrame = tk.Frame(self.loginWindow, width=1250, height=15, borderwidth=2)
        self.centerFrame.pack()
        self.frame2 = Frame(self.loginWindow)
        self.frame2.pack(pady=20)
        # Create a new frame
        self.frame = Frame(self.loginWindow)
        self.frame.pack(fill='both', expand=True)  # Adjust the fill and expand options

        # Create a canvas and a vertical scrollbar
        self.canvas = Canvas(self.frame)
        self.scrollbar = Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        # Configure the canvas to be scrollable
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind the scroll wheel event to the yview_scroll method
        # Bind the scroll wheel event to the root window
        self.loginWindow.bind("<MouseWheel>",
                              lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)),
                                                                     "units"))  # For Windows

        # Place the canvas and the scrollbar in the frame
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        booklist = db.get_books()  # This should return a list of tuples with book info

        for i, book in enumerate(booklist):
            book_id, book_name, book_cover, book_quantity,author,description = book

            temp_cover=book_cover
            book_cover="images\\"+book_cover
            # Open, resize, and display the book cover
            img = Image.open(book_cover)
            img = img.resize((150, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.scrollable_frame, image=img)
            img_label.image = img

            # Bind the function to the image label
            img_label.bind("<Button-1>", lambda event, command = lambda b_id=book_id,b_name=book_name,b_cover=temp_cover,b_q=book_quantity,b_aut=author,b_des=description: self.edit_book_window(username, b_id, b_name, b_cover, b_q, b_aut,b_des): command())


              # Don't forget to pack (or grid/place) the label

            # Keep a reference to the image

            # Create a label to display the book name
            #quantity_label = tk.Label(scrollable_frame, text=str(book_quantity), font=("Comic Sans MS", 15), fg="black")

            book_label = tk.Label(self.scrollable_frame, text=f"ID: {book_id}\n{book_name} \n Quantity:{str(book_quantity)}\nAuthor:{author}", font=("Comic Sans MS", 15), fg="black",
                                  wraplength=150)
            book_label.bind("<Button-1>", lambda event,
                                                command=lambda b_id=book_id, b_name=book_name, b_cover=temp_cover,
                                                               b_q=book_quantity, b_aut=author,
                                                               b_des=description: self.edit_book_window(username, b_id,
                                                                                                        b_name, b_cover,
                                                                                                        b_q, b_aut,
                                                                                                        b_des): command())

            # Determine the row and column for each book
            row = i // 2  # Integer division - each row will contain two books
            column = i % 2 * 3  # Each book takes up two columns (one for the image, one for the name)

            # Place the image and name in the correct row and column
            img_label.grid(row=row, column=column*2)
            book_label.grid(row=row, column=column*2 + 1)

            style = tkk.Style()

            # Assuming you're using the 'flatly' theme
            #style.theme_use('flatly')

            # Create a new style that inherits from 'TButton', and overrides the background option
            style.configure('TButton', background='white')

            plus_image = Image.open("resources/plus.png")
            plus_image = plus_image.resize((20, 20))
            plus_image = ImageTk.PhotoImage(plus_image)
            minus_image = Image.open("resources/minus.png")
            minus_image = minus_image.resize((20, 20))
            minus_image = ImageTk.PhotoImage(minus_image)

            plus_button = tkk.Button(self.scrollable_frame, image=plus_image,bootstyle="link", command=lambda b_id=book_id: [db.increase_book(b_id), self.admin(username)])
            plus_button.image = plus_image
            plus_button.grid(row=row, column=column * 2 + 2 )
            minus_button = tkk.Button(self.scrollable_frame, image=minus_image,bootstyle="link",command=lambda b_id=book_id: [db.decrease_book(b_id), self.admin(username)])
            minus_button.image = minus_image
            minus_button.grid(row=row, column=column*2+3)

    def mainWindow(self, username):
        # List of image paths
        ds.destruction(self)
        folder = "images\\"
        image_paths = []
        images_from_db = db.get_images_From_market()
        for image in images_from_db:
            image = list(image)
            image[0] = folder + image[0]
            image_paths.append(image)

        # scrollable_frame = MainWindow(self.loginWindow, image_paths, username)
        # scrollable_frame.pack(fill="both", expand=True)
        # Header frame and text
        self.topframe = tk.Frame(self.loginWindow)
        self.topframe.pack(side="top")

        self.header = tk.Label(self.topframe, text="WELCOME BACK", fg="black")
        self.header.config(font=("Times New Roman", 40))
        self.header.pack()

        # ----------------------------------------------
        # sdlkjghdfg;ldkjsfhg
        def open_link_1():
            webbrowser.open("https://www.example1.com")

            # Create a canvas and scrollbar

        self.centerFrame = tk.Frame(self.loginWindow, width=1250, height=17, borderwidth=2)
        self.centerFrame.pack()
        self.canvas = tk.Canvas(self.loginWindow, width=700, height=500)  # Adjust width and height as needed
        self.scrollbar = tk.Scrollbar(self.loginWindow, orient="vertical", command=self.canvas.yview)
        self.scrollbar_h = tk.Scrollbar(self.loginWindow, orient="horizontal", command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollbar_h.set)

        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar_h.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True, pady=20)

        # Create a frame inside the canvas to hold the images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor="nw")
        self.loginWindow.bind("<MouseWheel>",
                              lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)),
                                                                     "units"))  # For Windows

        # Add images to the image frame
        self.images = []
        i = 0
        j = 0  # For two columns, initialize j as 0
        self.added_labels = {}
        for image_path, book_name, book_author, id in image_paths:
            name, author = book_name, book_author
            row = i // 2  # Integer division - each row will contain 2 books
            col = j % 2 * 2
            img = Image.open(image_path)
            img = img.resize((130, 200))
            tk_img = ImageTk.PhotoImage(img)

            self.images.append(tk_img)
            self.label = tk.Label(self.image_frame, image=tk_img)
            self.label.grid(row=row, column=col, pady=10)

            self.txt = tk.Frame(self.image_frame)
            self.txt.grid(row=row, column=col + 1, padx=46)
            # book name
            self.bookName = tk.Label(self.txt, text=name, font=("Times New Roman", 20), wraplength=160)
            self.bookName.grid(row=0, column=0, pady=10)
            # hyperlinks of books names
            self.bookName.bind("<Button-1>", lambda event, command = lambda b_cover=image_path, a_id = id, usernamet = username: self.bookInfo(b_cover,name,author,a_id,usernamet): command())

            # author name
            self.bookAuthor = tk.Label(self.txt, text=f"By: {author}", font=("Times New Roman italic", 15), anchor="sw")
            self.bookAuthor.grid(row=1, column=0)

            # add to cart
            # add to cart
            self.cartbutton = tkk.Button(self.txt, text="add to cart", width=12,
                                        command=lambda b_id=id: [self.add_to_cart(username, b_id, "mainwindow")],
                                         style= "success")
            self.cartbutton.grid(row=2, column=0)

            # Create a label for each book and store it in the dictionary
            self.added_labels[id] = tk.Label(self.txt, font=("Times New Roman", 15), wraplength=140)
            self.added_labels[id].grid(row=3, column=0, pady=5)
            i+=1
            j+=1

        # Update the canvas scroll region
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # -------------------------------------------------------------------
        # search bar
        #self.searchbar = tk.Frame(self.topframe, width=1200, height=100)
        #self.searchbar.pack(side="bottom", fill="both")
        #self.lbl_search = tk.Label(self.searchbar, text="Search", font="Times 12 bold", bg="grey", fg="white")
        #self.lbl_search.grid(row=0, column=0)
        #self.ent_search = tk.Entry(self.searchbar, width=90)
        #
        #def on_entry_click(event):
        #    """Function to handle when the user clicks inside the entry."""

        #    if self.ent_search.get() == "Search Here":
        #        self.ent_search.delete(0, tk.END)  # Clear the placeholder text
        #        self.ent_search.config(fg='black')  # Change text color to black

        #def on_focus_out(event):
        #    """Function to handle when the self.ent_search loses focus."""

        #    if self.ent_search.get() == "":
        #        self.ent_search.insert(0, "Search Here")  # Restore placeholder text
        #        self.ent_search.config(fg='grey')  # Change text color to grey

        #def search():
        #   """Function to handle the search."""

        #   search_term = self.ent_search.get()
        #  print("Searching for:", search_term)

        #self.ent_search.bind("<FocusIn>", on_entry_click)
        #self.ent_search.bind("<FocusOut>", on_focus_out)

        # search button
        #self.search_button = tk.Button(self.searchbar, text="Search", command=search, width=7, height=1, bg="#217afa")
        #self.search_button.grid(row=0, column=0, padx=10, pady=5)

        # Perform search operation here
        #self.ent_search.insert(0, "Search here")
        #self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        # profile button
        self.profile_img = Image.open("resources/profile.png")
        self.profile_img = self.profile_img.resize((40, 40))
        self.profile_img = ImageTk.PhotoImage(self.profile_img)  # Store the image object in an instance variable
        self.profile_button = tkk.Button(self.loginWindow, command=lambda: self.profile(username), bootstyle="link",
                                         image=self.profile_img)
        self.profile_button.place(x=0, y=0)

        self.cart_img = Image.open("resources/face.png")
        self.cart_img = self.cart_img.resize((40, 40))
        self.cart_img = ImageTk.PhotoImage(self.cart_img)  # Store the image object in an instance variable
        self.cart_button = tkk.Button(self.loginWindow, command=lambda: self.cartwindow(username, self.cart),
                                      bootstyle="link",
                                      image=self.cart_img)
        self.cart_button.place(x=0, y=50)

        # sign out button
        self.sign_out_img = Image.open("resources/leaving.png")
        self.sign_out_img = self.sign_out_img.resize((50, 50))
        self.sign_out_img = ImageTk.PhotoImage(self.sign_out_img)
        self.sign_out_button = tkk.Button(self.loginWindow, bootstyle="link", image=self.sign_out_img,
                                          command=lambda: self.login_Window())
        self.sign_out_button.place(x=740, y=0)
        self.db_quantities = db.check_item_quantity()
        self.db_quantities = dict(self.db_quantities)
    def add_to_cart(self, user_name, id, place):
        item = [user_name, id]
        if (self.db_quantities[id] > 0):
            self.db_quantities[id] -= 1
            self.cart.append(item)
            if (place == "mainwindow"):
                self.added_labels[id].config(text="Added Successfully", fg="green")
                self.added_labels[id].after(1500, lambda: self.added_labels[id].config(text="", fg="black"))
            else:
                self.feedback.config(text="Added Successfully", fg="green")
                self.feedback.after(1500, lambda: self.feedback.config(text="", fg="black"))
        else:
            if (place == "mainwindow"):
                self.added_labels[id].config(text="Out Of Stock", fg="red")
                self.added_labels[id].after(1500, lambda: self.added_labels[id].config(text="", fg="black"))
            else:
                self.feedback.config(text="Out Of Stock", fg="red")
                self.feedback.after(3000, lambda: self.feedback.config(text="", fg="black"))

    def cartwindow(self, username, cart):
        self.cart_window = tk.Toplevel(self.loginWindow)
        self.cart_window.title('Cart Window')
        self.cart_window.geometry("800x900")
        self.cart_window.resizable(False, False)

        self.cartframe = tk.Frame(self.cart_window)
        self.cartframe.pack(side="top")

        self.header = tk.Label(self.cartframe, text="CART", fg="black")
        self.header.config(font=("Times New Roman", 40))
        self.header.pack()
        self.cartcanvas = tk.Canvas(self.cart_window, width=700, height=300)  # Adjust width and height as needed
        self.scrollbar1 = tk.Scrollbar(self.cart_window, orient="vertical", command=self.cartcanvas.yview)
        self.cartcanvas.config(yscrollcommand=self.scrollbar1.set, xscrollcommand=self.scrollbar_h.set)

        self.scrollbar1.pack(side="right", fill="y")

        self.cartcanvas.pack(side="left", fill="both", expand=True, pady=20)

        # Create a frame inside the canvas to hold the images
        self.cartimage_frame = tk.Frame(self.cartcanvas)
        self.cartcanvas.create_window((0, 0), window=self.cartimage_frame, anchor="nw")
        self.cartcanvas.bind_all("<MouseWheel>",
                                 lambda event: self.cartcanvas.yview_scroll(int(-1 * (event.delta / 120)),
                                                                            "units") if len(
                                     self.cart) > 0 else None)  # For Windows

        # Add images to the image frame
        self.cartimages = []
        k = 0
        a = 0  # For two columns, initialize j as 0
        ids = []
        for i in cart:
            ids.append(i[1])
        books = db.get_books_by_id(ids)
        if len(books) > 0:
            for bookNamedb, bookCoverdb, Quantitydb, Bookid in books:
                bookCoverdb = "images\\" + bookCoverdb
                row = a // 2  # Integer division - each row will contain 2 books
                col = k % 2 * 2
                img = Image.open(bookCoverdb)
                img = img.resize((130, 200))
                tk_img = ImageTk.PhotoImage(img)
                self.cartimages.append(tk_img)
                self.cartlabel = tkk.Label(self.cartimage_frame, image=tk_img)
                self.cartlabel.grid(row=row, column=col, pady=10)

                self.txtcart = tk.Frame(self.cartimage_frame)
                self.txtcart.grid(row=row, column=col + 1, padx=63)
                # book name
                self.cartbookName = tk.Label(self.txtcart, text=bookNamedb, font=("Times New Roman", 20),
                                             wraplength=140)
                self.cartbookName.grid(row=0, column=0, pady=10)

                self.remove_from_cart = tkk.Button(self.txtcart, text="remove from cart",
                                                  command=lambda c_id=Bookid: [remove_from_cart(username, c_id)]
                                                   ,style="danger",width=15)
                self.remove_from_cart.grid(row=2, column=0)

                k += 1
                a+=1
                # Move to the next column for the next set of books
            self.cartimage_frame.update_idletasks()
            self.cartcanvas.config(scrollregion=self.cartcanvas.bbox("all"))
            self.cart_confirm_button = tkk.Button(self.cart_window, text="Confirm The purchase",
                                                  command=lambda: buy(username, books)
                                                 ,style="success",width=20)
            self.cart_confirm_button.place(x=500, y=800)
            self.cart_clear_button = tkk.Button(self.cart_window, text="Empty Cart", command=lambda: emptycart(),
                                                style="warning")
            self.cart_clear_button.place(x=250, y=800)
        else:
            self.empty_massage = tkk.Label(self.cartimage_frame, text="No Books Found", foreground="Red",
                                           font=("Times New Roman", 50))
            self.empty_massage.grid(row=0, column=0, pady=350, padx=150)

        def emptycart():
            self.cart = []
            self.db_quantities = db.check_item_quantity()
            self.db_quantities = dict(self.db_quantities)
            self.cart_window.destroy()
            self.cartframe.destroy()
            self.cartwindow(username, self.cart)

        def remove_from_cart(username, id):
            removeitem = [username, id]
            for i in self.cart:
                if i[0] == removeitem[0] and i[1] == removeitem[1]:
                    self.cart.remove(i)
                    self.cart_window.destroy()
                    self.cartframe.destroy()
                    self.cartwindow(username, self.cart)

        def buy(username, books):
            conn = sqlite3.connect('book_store.db')
            c = conn.cursor()
            for book in books:
                book = list(book)
                c.execute("UPDATE books SET quantity = quantity - 1 WHERE id = ?", (book[3], ) )
                c.fetchone()
                c.execute("SELECT books_owned FROM users WHERE username = ?", (username,))
                userbooks = c.fetchone()
                userbooksstr = ""
                for i in userbooks:
                    userbooksstr += str(i)
                userbooksstr = userbooksstr + "," +str(book[3])
                c.execute("UPDATE users SET books_owned = ? WHERE username = ?", (userbooksstr,username,))
                c.fetchone()
                c.execute("INSERT INTO purchases (book_id, buyer_username) VALUES (?, ?)", (book[3], username,))
                c.fetchone()
                conn.commit()
            conn.close()
            self.cart_window.destroy()
            self.profile(username)

    def bookInfo(self, book, name, author, id,username,place=False):
        ds.destruction(self)
        self.loginWindow.bind("<MouseWheel>",
                              lambda event: None)
        self.canvas = tk.Canvas(self.loginWindow, width=800, height=900)
        self.scrollable_frame = tk.Frame(self.canvas)  # Create a new frame

        self.scrollbar = tk.Scrollbar(self.loginWindow, orient="vertical", command=self.canvas.yview)

        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, pady=20)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")  # Add the frame to the canvas

        img = Image.open(book)
        img = img.resize((300, 400))
        self.tk_img2 = ImageTk.PhotoImage(img)
        photo = tk.Label(self.scrollable_frame, image=self.tk_img2)  # Add the label to the frame
        photo.pack(side="top")

        # book name detail
        bookName = tk.Label(self.scrollable_frame, text=f"Book Name: {name}", font=("Times New Roman", 14),
                            justify="center")
        bookName.pack(side="top")

        # author name detail
        authorName = tk.Label(self.scrollable_frame, text=f"Author Name: {author}", font=("Times New Roman", 14),
                              justify="center")
        authorName.pack(side="top")

        # release date detail
        releaseDate = tk.Label(self.scrollable_frame, text="Release Year: 1978", justify="center",
                               font=("Times New Roman", 14))
        releaseDate.pack(side="top")

        line = tk.Label(self.scrollable_frame, text="-" * 128, justify="left")
        line.pack(side="top")

        describe = str(db.get_book_descreption(id)[0])

        content = tk.Label(self.scrollable_frame, text=describe, font=("Times New Roman", 14),
                           justify="center", wraplength=760)  # Add the label to the frame
        content.pack(side="top", padx= 10, fill="x")

        if not place:
            button1 = tkk.Button(self.scrollable_frame, text="Add to cart",
                                 command=lambda : self.add_to_cart(username, id, "bookinfo"),
                                 style="dark")
            button1.pack(side="left", padx=10, pady=5, expand = True)

            button2 = tkk.Button(self.scrollable_frame, text="Go back", command=lambda : self.mainWindow(username)
                                 , style="dark", width=10)
            button2.pack(side="right", padx=10, pady=5, expand = True)

            self.feedback = tk.Label(self.scrollable_frame, font=("Times New Roman", 30))
            self.feedback.pack(side= "bottom", pady= 20)
        else:
            button2 = tkk.Button(self.scrollable_frame, text="Go back", command=lambda: self.profile(username)
                                 , style="dark", width=10)
            button2.pack(expand=True,pady=10)

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def reading(self):
        new_window = tk.Toplevel(self.loginWindow)
        new_window.title("Reading")
        new_window.geometry("400x400")
        new_window.resizable(False, False)
        label = tkk.Label(new_window,
                          text="You should be able to read a PDF book here, but the deadline is 2 days later, so what are you talking about?\n :)",
                          wraplength=300, font=("Comic Sans MS", 20), foreground="red", anchor="center",
                          justify="center")
        label.pack(expand=True)
