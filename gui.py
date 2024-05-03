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

        quantity_label = tkk.Label(new_window, text="Quantity", font=("Comic Sans MS", 12))
        quantity_label.grid(row=2, column=0)
        quantity_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        quantity_entry.grid(row=2, column=1)

        author_label = tkk.Label(new_window, text="Author", font=("Comic Sans MS", 12))
        author_label.grid(row=3, column=0)
        author_entry = tkk.Entry(new_window, font=("Comic Sans MS", 10))
        author_entry.grid(row=3, column=1)

        # Function to add the book to the database
        def add_book_to_db():
            name = name_entry.get()
            cover = cover_entry.get()
            quantity = quantity_entry.get()
            author = author_entry.get()
            db.add_book(name, cover, quantity,author)

        # Create an 'Add Book' button
        add_button = tk.Button(new_window, text="Add Book", font=("Comic Sans MS", 12), foreground="blue",
                               command=lambda:[add_book_to_db(),new_window.destroy(),self.admin(username)])
        add_button.grid(row=4, column=0, columnspan=2)

    def destruction(self):
        try:
            self.app.destroy()
        except Exception as e:
            pass

        try:
            self.frame.destroy()
        except Exception as e:
            pass

        try:
            self.username_entry.destroy()
        except Exception as e:
            pass

        try:
            self.username_label.destroy()
        except Exception as e:
            pass

        try:
            self.password_entry.destroy()
        except Exception as e:
            pass

        try:
            self.password_label.destroy()
        except Exception as e:
            pass

        try:
            self.login_button.destroy()
        except Exception as e:
            pass

        try:
            self.invalid.destroy()
        except Exception as e:
            pass

        try:
            self.createuser.destroy()
        except Exception as e:
            pass

        try:
            self.newname_label.destroy()
        except Exception as e:
            pass

        try:
            self.newname_entry.destroy()
        except Exception as e:
            pass

        try:
            self.duplicate.destroy()
        except Exception as e:
            pass

        try:
            self.signup_button.destroy()
        except Exception as e:
            pass

        try:
            self.success.destroy()
        except Exception as e:
            pass

        try:
            self.tologin_button.destroy()
        except Exception as e:
            pass

        try:
            self.img.destroy()
        except Exception as e:
            pass

        try:
            self.signout_img.destroy()
        except Exception as e:
            pass

        try:
            self.imglabel.destroy()
        except Exception as e:
            pass

        try:
            self.frame2.destroy()
        except Exception as e:
            pass

        try:
            self.add_book_button.destroy()
        except Exception as e:
            pass
        try:
            self.signout_button.destroy()
        except Exception as e:
            pass
        try:
            self.remove_book_button.destroy()
        except Exception as e:
            pass
        try:
            self.refresh_button.destroy()
        except Exception as e:
            pass
        try:
            self.centerFrame.destroy()
        except Exception as e:
            pass
        try:
            self.manage_members_button.destroy()
        except Exception as e:
            pass
        try:
            self.namelocation.destroy()
        except Exception as e:
            pass
        try:
            self.namelabel.destroy()
        except Exception as e:
            pass
        try:
            self.scrollable_frame.destroy()
        except Exception as e:
            pass
    def login_Window(self):
        self.destruction()
        self.loginWindow.geometry('800x900')
        self.loginWindow.title('Login')
        self.loginWindow.resizable(False, False)

        self.app = Application("resources/topbar.gif",25,50,master=self.loginWindow)
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
        try:
            self.unauthorized.destroy()
        except:
            pass
        self.destruction()
        self.loginWindow.title('Create Account')
        self.app = Application("resources/welcome-anime.gif",22,90, master=self.loginWindow)
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
        self.img = Image.open("resources/download.jpeg")
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

        booklist = db.get_user_books(username)  # This should return a list of tuples with book info

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
        self.destruction()

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
        self.refresh_button.place(x=675, y=115)
        self.centerFrame = tk.Frame(self.loginWindow, width=1250, height=15, borderwidth=2)
        self.centerFrame.pack()
        self.frame2 = Frame(self.loginWindow)
        self.frame2.pack(pady=20)
        # Create a new frame
        self.frame = Frame(self.loginWindow)
        self.frame.pack(fill='both', expand=True)  # Adjust the fill and expand options

        # Create a canvas and a vertical scrollbar
        canvas = Canvas(self.frame)
        scrollbar = Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        # Configure the canvas to be scrollable
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
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
            book_id, book_name, book_cover, book_quantity,author = book
            book_cover="images\\"+book_cover
            # Open, resize, and display the book cover
            img = Image.open(book_cover)
            img = img.resize((150, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(self.scrollable_frame, image=img)
            img_label.image = img  # Keep a reference to the image

            # Create a label to display the book name
            #quantity_label = tk.Label(scrollable_frame, text=str(book_quantity), font=("Comic Sans MS", 15), fg="black")

            book_label = tk.Label(self.scrollable_frame, text=f"ID: {book_id}\n{book_name} \n Quantity:{str(book_quantity)}\nAuthor:{author}", font=("Comic Sans MS", 15), fg="black",
                                  wraplength=150)

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

    def mainWindow(self,username):
        # List of image paths
        folder = "images\\"
        image_paths = []
        images_from_db = db.get_images_From_market()
        for image in images_from_db:
            image = list(image)
            image[0] = folder + image[0]
            image_paths.append(image)

        #scrollable_frame = MainWindow(self.loginWindow, image_paths, username)
        #scrollable_frame.pack(fill="both", expand=True)
        # Header frame and text
        topframe = tk.Frame(self.loginWindow)
        topframe.pack(side="top")

        header = tk.Label(topframe, text="WELCOME BACK", fg="black")
        header.config(font=("Times New Roman", 40))
        header.pack()

        # ----------------------------------------------
        #sdlkjghdfg;ldkjsfhg 
        def open_link_1():
            webbrowser.open("https://www.example1.com")

            # Create a canvas and scrollbar

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

        # Add images to the image frame
        self.images = []
        i = 0
        j = 0  # For two columns, initialize j as 0

        for image_path, book_name, book_author, id in image_paths:
            name, author = book_name, book_author

            img = Image.open(image_path)
            img = img.resize((130, 200))
            tk_img = ImageTk.PhotoImage(img)
            self.images.append(tk_img)
            label = tk.Label(self.image_frame, image=tk_img)
            label.grid(row=i, column=j, pady=10)

            txt = tk.Frame(self.image_frame)
            txt.grid(row=i, column=j + 1, padx=10)  # Adjust column for author, buttons, etc.

            # book name
            bookName = tk.Label(txt, text=name, font=("Times New Roman", 11))
            bookName.grid(row=0, column=0, pady=10)

            # author name
            bookAuthor = tk.Label(txt, text=f"By: {author}", font=("Times New Roman italic", 10), anchor="sw")
            bookAuthor.grid(row=1, column=0)

            # add to cart
            cart = tk.Button(txt, text="add to cart", width=12, height=1,
                             command=lambda b_id=id: [self.add_to_cart(username, b_id),print(b_id)])
            cart.grid(row=2, column=0)

            i += 1
            if i % 4 == 0:  # Change to 6 for two columns, adjust as needed
                i = 0
                j += 2  # Move to the next column for the next set of books

        # Update the canvas scroll region
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # -------------------------------------------------------------------
        # search bar
        searchbar = tk.Frame(topframe, width=1200, height=100)
        searchbar.pack(side="bottom", fill="both")
        self.lbl_search = tk.Label(searchbar, text="Search", font="Times 12 bold", bg="grey", fg="white")
        self.lbl_search.grid(row=0, column=0)
        self.ent_search = tk.Entry(searchbar, width=90)

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
        search_button = tk.Button(searchbar, text="Search", command=search, width=7, height=1, bg="#217afa")
        search_button.grid(row=0, column=0, padx=10, pady=5)

        # Perform search operation here
        self.ent_search.insert(0, "Search here")
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

        # profile button
        profile_img = Image.open("resources/profile.png")
        profile_img = profile_img.resize((40, 40))
        self.profile_img = ImageTk.PhotoImage(profile_img)  # Store the image object in an instance variable
        profile_button = tkk.Button(self.loginWindow, command=open_link_1,bootstyle="link", image=self.profile_img)
        profile_button.place(x=0, y=0)

        # sign out button
        sign_out_img = Image.open("resources/leaving.png")
        sign_out_img = sign_out_img.resize((50, 50))
        self.sign_out_img = ImageTk.PhotoImage(sign_out_img)
        sign_out_button = tkk.Button(self.loginWindow, bootstyle="link",image=self.sign_out_img, command=open_link_1)
        sign_out_button.place(x=740, y=0)

    def add_to_cart(self,user_name, id):
        item = [user_name, id]
        self.cart.append(item)
        print(self.cart)


