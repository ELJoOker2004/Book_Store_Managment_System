from tkinter import ttk

import gui
import ttkbootstrap as tkk
import db_functions as db
import sqlite3
import tkinter as tk
import pygame





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #db.add_user("admin","admin","Main Admin")
    #db.add_book("Practical Malware Analysis","pma.png",5)
    # pygame.mixer.init()
    # pygame.mixer.music.load('peak.mp3')
    # pygame.mixer.music.set_volume(.1)
    # pygame.mixer.music.play(0)
    root = tkk.Window()
    app = gui.Gui(root)
    root.mainloop()

