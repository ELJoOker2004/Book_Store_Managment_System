
import db_functions as db

import test
import sys
import sqlite3



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

def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        if db.login(username, password):
            print("Login successful!")
        else:
            print("Login failed. Please check your username and password.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
    print("Fuck Omar")
    db.printRowInTable("Alice")
    #insertRowInTable("eljooker", 19)
    db.printRowInTable("eljooker")
    db.deleteRowInTable(2)
