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
        topFrame =tk.Frame(mainFrame, width=1350, height=50, relief="sunken", borderwidth=2)
        topFrame.pack()

        #center frame
        centerFrame = tk.Frame(mainFrame, width=1350, height = 680, relief="ridge")
        centerFrame.pack()

        #center left frame
        centerLeftFrame = tk.Frame(centerFrame, width=100,height = 700, borderwidth=2, relief="sunken",bg="grey")
        centerLeftFrame.pack(side="left")

        #center right frame
        centerRightFrame = tk.Frame(centerFrame, width=1250,height = 700, borderwidth=2, relief="sunken")
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
        search_button.grid(row=0, column=0, padx=10, pady=5)


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
            label.bind("<Enter>", lambda event:label.config(cursor="hand2"))
            label.bind("<Leave>",label.config(cursor="arrow"))

        leftpanel = tk.Label(centerLeftFrame, bg = "grey",width = 10, height=700)  
        leftpanel.pack()  

        #header of the main page
        header= tk.Label(topFrame, text= "WELCOME BACK", fg="black",width= 1350)
        header.config(font=("Times New Roman", 36),pady= 10)
        header.pack()

        #first 6 books in 2 coulumns
        book_detail = [("D:\python\images\\to kill a mocking bird.png","To Kill a Mocking Bird", "Harper Lee"),
                       ("D:\python\images\inheritance games.jpeg", "The Inheritance Games", "Jennifer Lynn Barnes"), 
                       ("D:\python\images\great expdition.jpeg", "The Great Expedtiton","Charles Dickens"),
                       ("D:\python\images\cant touch me.jpeg", "Cant't Touch Me ", "David Goggins"),
                       ("D:\python\images\\book thief.jpeg", "The Book Thief", "Markus Zusak"),
                       ("D:\python\images\\48 laws of power.jpg","48 Laws of Power", "Robert Greene")
                       
                       ]
        
        for i, book in enumerate(book_detail):
            
            book_path, book_name, author = book
            # Calculate the row and column based on the index
            row = i // 2  # Integer division gives the row number
            col = i % 2  # Remainder gives the column number

            # Create a label to display the book name
            book_label = tk.Label(centerFrame, text=book_name, font=("Times New Roman", 13), fg="black",
                                  wraplength=250)
            
            #hyperlinks of books names
            book_label.bind("<Button-1>", lambda event, cmd=open_link_1: cmd())
            book_label.bind("<Enter>", book_label.config(cursor="hand2", fg="blue"))
            book_label.bind("<Leave>", lambda event: book_label.config(cursor="arrow", fg="black"))

            #coordinates of books labels
            book_label.place(x=250 + col * 170 * 2.2,
                             y=170 + row * 210)  # Adjust the x and y coordinates based on the row and column
            
            # Create a label to display the book name
            author_label = tk.Label(centerFrame, text=f"By: {author}", font=("Times New Roman italic", 13), fg="black",
                                  wraplength=250)
            author_label.place(x=250 + col * 170 * 2.2,
                             y=200 + row * 210)  # Adjust the x and y coordinates based on the row and column

            # Open, resize, and display the book cover
            img = Image.open(book_path)
            img = img.resize((150, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(centerFrame, image=img)
            img_label.image = img  # Keep a reference to the image
            img_label.place(x=90 + col * 170 * 2.2,
                            y=70 + row * 210)  # Adjust the x and y coordinates based on the row and column
                      
        #second 3 books in 1 coulumn
        book_detail = [
            ("D:\python\images\\art of war.png","The art of War", "Sun Tzu"),
            ("D:\python\images\pride and pejudice.jpeg", "Pride and Prejudice", "Jane Austen"),
            ("D:\python\images\\the hobbit.jpeg", "The Hobbit", "J.J.R. Tolkien"),
            ("D:\python\images\moby dick.jpeg", "Moby Dick ", "Herman Melvilla"),
            ("D:\python\images\\rich dad poor dad.jpeg", "Ruch Dad Poor Dad", "Robert T. Kiyosaki"),
            ("D:\python\images\lord of the rings.jpeg","Lord if the Rings", "J.J.R. Tolkien")
        ]
        for i, book in enumerate(book_detail):
            
            book_path, book_name, author = book
            # Calculate the row and column based on the index
            row = i // 2  # Integer division gives the row number
            col = i % 2  # Remainder gives the column number

            # Create a label to display the book name
            book_label = tk.Label(centerFrame, text=book_name, font=("Times New Roman", 13), fg="black",
                                  wraplength=250)
            
            #hyperlink for book name
            book_label.bind("<Button-1>", lambda event, cmd=open_link_1: cmd())
            book_label.bind("<Enter>", book_label.config(cursor="hand2", fg="blue"))
            book_label.bind("<Leave>", lambda event: book_label.config(cursor="arrow", fg="black"))

            #coordinates of the books' labels
            book_label.place(x=1010 + col * 170 * 2.2,
                             y=170 + row * 210)  # Adjust the x and y coordinates based on the row and column
            
            # Create a label to display the book author
            author_label = tk.Label(centerFrame, text=f"By: {author}", font=("Times New Roman italic", 13), fg="black",
                                  wraplength=250)
            author_label.place(x=1010 + col * 170 * 2.2,
                             y=200 + row * 210)  # Adjust the x and y coordinates based on the row and column

            # Open, resize, and display the book cover
            img = Image.open(book_path)
            img = img.resize((150, 200))  # Resize the image
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(centerFrame, image=img)
            img_label.image = img  # Keep a reference to the image
            img_label.place(x=850 + col * 170 * 2.2,
                            y=70 + row * 210)  # Adjust the x and y coordinates based on the row and column

            
def main():

    win = tk.Tk()
    win.geometry("1300x750+350+200")
    win.title("Main Window")
    app = Main(win)

    win.mainloop()

main()

#-------------------------------------------

