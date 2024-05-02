import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import os
import webbrowser





class MainWindow(tk.Frame):
    def __init__(self, master, image_paths, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        

        #Header frame and text
        topframe = tk.Frame(self)
        topframe.pack(side="top")

        header= tk.Label(topframe, text= "WELCOME BACK", fg="black")
        header.config(font=("Times New Roman", 48))
        header.pack()

#----------------------------------------------
        def open_link_1():
            webbrowser.open("https://www.example1.com")  
        
        # Create a canvas and scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True, pady=20)
        
        # Create a frame inside the canvas to hold the images
        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.image_frame, anchor="nw")
        
        # Add images to the image frame
        self.images = []
        i = 0
        j = 150
        
        for image_path, book_name, book_author  in image_paths:
            
            name, author = book_name, book_author

            img = Image.open(image_path)
            img = img.resize((170, 230))
            tk_img = ImageTk.PhotoImage(img)
            self.images.append(tk_img)
            label = tk.Label(self.image_frame, image=tk_img)
            label.grid(row = i, column = 0, pady=10)
            
            txt = tk.Frame(self.image_frame)
            txt.grid(row=i, column=100,padx=10)
            
            # book name
            bookName = tk.Label(txt, text=name, font=("Times New Roman", 15))
            bookName.grid(row=i,column=100, pady=10)
            # hyperlinks of books names
            bookName.bind("<Button-1>", lambda event, cmd=open_link_1: cmd())
            bookName.bind("<Enter>", bookName.config(cursor="hand2", fg="blue"))
            bookName.bind("<Leave>", lambda event: bookName.config(cursor="arrow", fg="black"))

            # author name
            bookAuthor = tk.Label(txt, text=f"By: {author}", font=("Times New Roman italic", 13),anchor="sw" )
            bookAuthor.grid(row=i+10, column=100)
            
            i += 150

        i = 0
        for image_path, book_name, book_author  in image_paths:
            
            name, author = book_name, book_author

            img = Image.open(image_path)
            img = img.resize((170, 230))
            tk_img = ImageTk.PhotoImage(img)
            self.images.append(tk_img)
            label = tk.Label(self.image_frame, image=tk_img)
            label.grid(row = i, column = j, pady=10)
            
            txt = tk.Frame(self.image_frame)
            txt.grid(row=i, column=100+j,padx=10)
            
            # book name
            bookName = tk.Label(txt, text=name, font=("Times New Roman", 15))
            bookName.grid(row=i,column=100+j, pady=10)
            # hyperlinks of books names
            bookName.bind("<Button-1>", lambda event, cmd=open_link_1: cmd())
            bookName.bind("<Enter>", bookName.config(cursor="hand2", fg="blue"))
            bookName.bind("<Leave>", lambda event: bookName.config(cursor="arrow", fg="black"))

            # author name
            bookAuthor = tk.Label(txt, text=f"By: {author}", font=("Times New Roman italic", 13),anchor="sw" )
            bookAuthor.grid(row=i+10, column=100+j)
            
            i += 150
            

            
            
        
        # Update the canvas scroll region
        self.image_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
#-------------------------------------------------------------------
        #search bar
        searchbar = tk.Frame(topframe, width=1200, height= 100)
        searchbar.pack(side = "bottom",fill= "both")
        self.lbl_search = tk.Label(searchbar,text="Search", font = "Times 12 bold", bg = "grey", fg = "white")
        self.lbl_search.grid(row = 0, column=0)
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

        #search button
        search_button = tk.Button(searchbar, text="Search", command=search, width=7, height=1, bg="#217afa")
        search_button.grid(row=0, column=0, padx=10, pady=5)


        # Perform search operation here
        self.ent_search.insert(0,"Search here")
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)




if __name__ == "__main__":

    win = tk.Tk()
    win.geometry("700x800")
    win.title("Main Window")

    # List of image paths
    image_paths = [
            ("D:\python\images\\to kill a mocking bird.png","To Kill a Mocking Bird", "Harper Lee"),
            ("D:\python\images\inheritance games.jpeg", "The Inheritance Games", "Jennifer Lynn Barnes"), 
            ("D:\python\images\great expdition.jpeg", "The Great Expedtiton","Charles Dickens"),
            ("D:\python\images\cant touch me.jpeg", "Cant't Touch Me ", "David Goggins"),
            ("D:\python\images\\book thief.jpeg", "The Book Thief", "Markus Zusak"),
            ("D:\python\images\\48 laws of power.jpg","48 Laws of Power", "Robert Greene"),
            ("D:\python\images\\art of war.png","The art of War", "Sun Tzu"),
            ("D:\python\images\pride and pejudice.jpeg", "Pride and Prejudice", "Jane Austen"),
            ("D:\python\images\\the hobbit.jpeg", "The Hobbit", "J.J.R. Tolkien"),
            ("D:\python\images\moby dick.jpeg", "Moby Dick ", "Herman Melvilla"),
            ("D:\python\images\\rich dad poor dad.jpeg", "Ruch Dad Poor Dad", "Robert T. Kiyosaki"),
            ("D:\python\images\lord of the rings.jpeg","Lord if the Rings", "J.J.R. Tolkien")
                       
                    ]

    # Create the scrollable image frame
    scrollable_frame = MainWindow(win, image_paths)
    scrollable_frame.pack(fill="both", expand=True)

    win.mainloop()
