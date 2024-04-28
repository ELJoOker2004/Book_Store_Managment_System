import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import os
import webbrowser


class Main(object):
    def __init__(self,master):
        self.master = master

        #frames
        mainFrame= tk.Frame(self.master)
        mainFrame.pack()
    
        #Top frame
        topFrame =tk.Frame(mainFrame, width=1350, height=50, padx=10, relief="sunken", borderwidth=2)
        topFrame.pack()

        #center frame
        centerFrame = tk.Frame(mainFrame, width=1350, height = 680, relief="ridge",bg="red")
        centerFrame.pack()

        #center left frame
        centerLeftFrame = tk.Frame(centerFrame, width=100,height = 700, borderwidth=2, relief="sunken",bg="grey")
        centerLeftFrame.pack(side="left")

        #center right frame
        centerRightFrame = tk.Frame(centerFrame, width=1250,height = 700, borderwidth=2, relief="sunken", bg="orange")
        centerRightFrame.pack()
        
        #search bar
        searchbar = tk.LabelFrame(centerRightFrame, width=1200, height= 100, bg = "white")
        searchbar.pack(fill= "both")
        self.lbl_search = tk.Label(searchbar,text="Search", font = "Times 12 bold", bg = "grey", fg = "white")
        self.lbl_search.grid(row = 0, column=0)
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
        #search button
        search_button = tk.Button(searchbar, text="Search", command=search, width=7, height=1)
        search_button.grid(row=0, column=0, padx=(3, 10), pady=5)


        # Perform search operation here
        self.ent_search.insert(0,"Search here")
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)


        #hyperlinks for the left side
        def open_link_1():
            webbrowser.open("https://www.example1.com")

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
            label = tk.Label(centerLeftFrame, text=text, fg="black", cursor="arrow", bg="grey",width=10)
            label.pack(pady=5)
            label.bind("<Button-1>", lambda event, cmd=command: cmd())

            # Change cursor when hovering over the label
            label.bind("<Enter>", label.config(cursor="hand2"))
            label.bind("<Leave>", lambda event: label.config(cursor="arrow"))

        leftpanel = tk.Label(centerLeftFrame, bg = "grey",width = 10, height=700)  
        leftpanel.pack()  

        #header of the main page
        header= tk.Label(topFrame, text= "WELCOME BACK", fg="black",width= 1350)
        header.config(font=("Times New Roman", 48),pady= 30)
        header.pack()

        # books = tk.LabelFrame(centerRightFrame, width= 1250, height=600, bg="green")
        # books.pack()
                      


def main():

    win = tk.Tk()
    win.geometry("1300x750+350+200")
    win.title("Main Window")
    app = Main(win)

    win.mainloop()

main()

#-------------------------------------------
