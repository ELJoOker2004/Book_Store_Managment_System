import tkinter as tk
from  tkinter import ttk
import sqlite3
from PIL import ImageTk, Image
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
        self.login_button = tk.Button(self.loginWindow, text="Login", command=self.profile)

        self.login_button.grid(row=2, columnspan=2, pady=10)
        self.loginWindow.mainloop()
        self.username_entry.destroy()
    def profile(self):

        self.username_entry.destroy()
        self.username_label.destroy()
        self.password_entry.destroy()
        self.password_label.destroy()
        self.login_button.destroy()

        self.img = Image.open("download.jpeg")
        # Resize the image
        self.img = self.img.resize((100, 100))
        self.img = ImageTk.PhotoImage(self.img)
        # Create a label and add the image to it
        imglabel = tk.Label(self.loginWindow, image=self.img)
        imglabel.grid(row=0, column=0, sticky='nw')


        # Connect to the SQLite database
        conn = sqlite3.connect('book_store.db')
        c = conn.cursor()
        # Execute a SQL query to get the name (assuming the name is in the third column and we're getting the first row)
        c.execute("SELECT * FROM users LIMIT 1")
        user = c.fetchone()
        username = user[2]  # Get the name from the third column
        # Create a label to display the name
        namelocation = tk.Label(self.loginWindow, text="Name:", font=("Comic Sans MS", 20), fg="brown")
        namelocation.place(x=120, y=5)
        namelabel = tk.Label(self.loginWindow, text=username, font=("Comic Sans MS", 15), fg="black")
        namelabel.place(x=130, y=45)

        #self.window.mainloop()
    # sub menu
    # file_menu = tk.Menu(menu, tearoff=False)
    # file_menu.add_command(label='New', command=lambda: print('New file'))
    # file_menu.add_command(label='Open', command=lambda: print('Open file'))
    # file_menu.add_separator()
    # menu.add_cascade(label='File', menu=file_menu)
    #
    # # another sub menu
    # help_menu = tk.Menu(menu, tearoff=False)
    # help_menu.add_command(label='Help entry', command=lambda: print(help_check_string.get()))
    #
    # help_check_string = tk.StringVar()
    # help_menu.add_checkbutton(label='check', onvalue='on', offvalue='off', variable=help_check_string)
    #
    # menu.add_cascade(label='Help', menu=help_menu)
    #
    # # add another menu to the main menu, this one should have a sub menu
    # # try to read the website below and add a submenu
    # # docs: https://www.tutorialspoint.com/python/tk_menu.htm
    # exercise_menu = tk.Menu(menu, tearoff=False)
    # exercise_menu.add_command(label='exercise test 1')
    # menu.add_cascade(label='Exercise', menu=exercise_menu)
    #
    # exercise_sub_menu = tk.Menu(menu, tearoff=False)
    # exercise_sub_menu.add_command(label='some more stuff')
    # exercise_menu.add_cascade(label='more stuff', menu=exercise_sub_menu)
    #
    # window.configure(menu=menu)
    #
    # # menu button
    # menu_button = ttk.Menubutton(window, text='Menu Button')
    # menu_button.pack()
    #
    # button_sub_menu = tk.Menu(menu_button, tearoff=False)
    # button_sub_menu.add_command(label='entry 1', command=lambda: print('test 1'))
    # button_sub_menu.add_checkbutton(label='check 1')
    # # menu_button.configure(menu = button_sub_menu)
    # menu_button['menu'] = button_sub_menu

    # run

