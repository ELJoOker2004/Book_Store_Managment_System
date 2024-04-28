from tkinter import ttk

import gui
import ttkbootstrap as tkk
import db_functions as db
import sqlite3
import tkinter as tk




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #db.add_user("1","1","test user")
    #db.add_book("Practical Malware Analysis","pma.png",5)
    root = tkk.Window()
    app = gui.Gui(root)
    root.mainloop()

