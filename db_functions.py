import sqlite3
import hashlib
def insertRowInTable(name, age):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Insert rows into the table
    cursor.execute("INSERT INTO my_table (name, age) VALUES (?, ?)", (name, age))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def deleteRowInTable(id):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM my_table WHERE id = ?", (id,))
    print(f"Row with ID {id} deleted successfully.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def printRowInTable(n):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM my_table WHERE name = ?", (n,))
    row = cursor.fetchone()

    if row:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Age: {row[2]}")
    else:
        print(f"No record found for {n}.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(username, password):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return True
    else:
        return False


def add_user(username, password):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))

    conn.commit()
    conn.close()
