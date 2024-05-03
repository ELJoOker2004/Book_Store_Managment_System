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
    role = "member"
    try:
        cursor.execute("INSERT INTO users (username, password, name,role) VALUES (?, ?, ?,?)", (username, hashed_password, name,role))
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

def add_book(name, cover, quantity,author):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (name, cover, quantity,author) VALUES (?, ?, ?,?)", (name, cover, quantity,author))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT id,name, cover, quantity,author FROM books")
    books = c.fetchall()
    conn.close()
    return books

def get_user_books(username):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT book_id FROM purchases WHERE buyer_username = ?", (username,))
    books_ids = c.fetchall()
    user_books = []
    for book_id in books_ids:
        c.execute("SELECT name, cover, quantity FROM books WHERE id = ?", (book_id[0],))
        book = c.fetchone()
        user_books.append(book)
    conn.close()
    return user_books

def increase_book(book_id):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("UPDATE books SET quantity = quantity + 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def decrease_book(book_id):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("UPDATE books SET quantity = quantity - 1 WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

def get_book_quantity(book_id):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT quantity FROM books where id = ?", (book_id,))
    quantity = c.fetchone()
    conn.close()
    #print(quantity)
    return quantity
def get_images_From_market():
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT cover, name, author, id  FROM books")
    books_paths = c.fetchall()
    conn.close()
    return books_paths
def delete_book(id):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.commit()
    conn.close()

def show_members():
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()

    # Get all users
    c.execute("SELECT username, name, books_owned, role FROM users")
    users = c.fetchall()

    conn.close()
    return users

def change_role(role, username):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()

    # Update the role of the specified user
    c.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))

    conn.commit()  # Commit the changes
    conn.close()
def delete_book(id):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    user = cursor.fetchone()
    conn.commit()
    conn.close()

def show_members():
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()

    # Get all users
    c.execute("SELECT username, name, books_owned, role FROM users")
    users = c.fetchall()

    conn.close()
    return users

def change_role(role, username):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()

    # Update the role of the specified user
    c.execute("UPDATE users SET role = ? WHERE username = ?", (role, username))

    conn.commit()  # Commit the changes
    conn.close()
def check_item_quantity(item):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    id = item[1]
    c.execute("SELECT quantity FROM books WHERE id = ?", (id,))
    quantity = c.fetchone()
    conn.close()
    if (quantity[0] == 0):
        return False
    return True