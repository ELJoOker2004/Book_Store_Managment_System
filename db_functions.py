import sqlite3
import hashlib

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

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

def add_book(name, cover, quantity,author,description):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (name, cover, quantity,author,descreption) VALUES (?, ?, ?,?,?)", (name, cover, quantity,author,description))
    conn.commit()
    conn.close()

def edit_book(book_id, name, cover, quantity, author, description):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute(" UPDATE books SET name = ?, cover = ?, quantity = ?, author = ?, descreption = ? WHERE id = ?", (name, cover, quantity, author, description, book_id))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT id,name, cover, quantity,author,descreption FROM books")
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
        c.execute("SELECT id,name, cover, quantity,author,descreption FROM books WHERE id = ?", (book_id[0],))
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
    if get_book_quantity(book_id)[0] >0:
        print(get_book_quantity(book_id)[0])
        c.execute("UPDATE books SET quantity = quantity - 1 WHERE id = ?", (book_id,))
    else:
        return False
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
def check_item_quantity():
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT id, quantity FROM books ",)
    quantity = c.fetchall()
    conn.close()
    return quantity
def get_books_by_id(cartids):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    books = []
    for cartid in cartids:
        c.execute("SELECT name, cover, quantity, id FROM books WHERE id = ?", (cartid,))
        book = c.fetchone()
        books.append(book)
    conn.close()
    return books
def get_book_descreption(id):
    conn = sqlite3.connect('book_store.db')
    c = conn.cursor()
    c.execute("SELECT descreption FROM books WHERE id = ?", (id,))
    book = c.fetchone()
    conn.close()
    return book
