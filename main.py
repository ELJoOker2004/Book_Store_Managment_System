import test
import db_functions as db
import sqlite3
import tkinter as tk


def create_users_table():
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = tk.Tk()
    app = test.gui(root)
    root.mainloop()

