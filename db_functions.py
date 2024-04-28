import sqlite3
import hashlib
def insertRowInTable(name):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Insert rows into the table
    cursor.execute("INSERT INTO users (name) VALUES (?, ?)", (name,))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def insertRowInTable(name):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Insert rows into the table
    cursor.execute("INSERT INTO users (name) VALUES (?, ?)", (name,))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def deleteRowInTable(username):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        print(f"Row with username {username} deleted successfully.")
    else:
        print(f"couldn't find row with username {username}.")
    # Commit changes and close the connection
    conn.commit()
    conn.close()


def searchByUsername(n):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE username = ?", (n,))
    row = cursor.fetchone()

    userlist = []
    userlist.append(row[0])
    userlist.append(row[2])
    userlist.append(row[3])

    conn.commit()
    conn.close()

    if row:
        return userlist
    else:
        return None

    # Commit changes and close the connection

def authenticateUser(username, password):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is None:
        #print("No user found with this username.")
        conn.close()
        return False
    elif row[1] == hash_password(password):
        conn.commit()
        conn.close()
        return True

def checkUserduplicates(username):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return True
    else:
        return False
def printRowInTable(n):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM users WHERE username = ?", (n,))
    row = cursor.fetchone()

    if row:

        print(f"Name: {row[2]}")

    else:
        print(f"No record found for {n}.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()

    conn.close()

    try:
        if user:
            print("Login successful!")
        else:
            print("Login failed. Please check your username and password.")
    except Exception as e:
        print(f"An error occurred: {e}")




def add_user(username, password,name):
    if (username == "" or password == "" or name == ""):
        return False
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password, name) VALUES (?, ?, ?)", (username, hashed_password, name))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def isAdmin(username):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    admin ="admin"
    try:
        cursor.execute("SELECT * FROM users WHERE username = ? AND role = ?", (username, admin))
        user = cursor.fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {e}")

def add_book(name, cover, quantity):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (name, cover, quantity) VALUES (?, ?, ?)", (name, cover, quantity))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT name, cover, quantity FROM books")
    books = c.fetchall()
    conn.close()
    return books
