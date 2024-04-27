import test
import sqlite3


def insertRowInTable(name, age):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Insert rows into the table
    cursor.execute("INSERT INTO my_table (name, age) VALUES (?, ?)", (name, age))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def printRowInTable(n):
    db_path = "book_store.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert rows into the table
    # cursor.execute("INSERT INTO my_table (name, age) VALUES (?, ?)", ("Alice", 30))


    cursor.execute(f"SELECT * FROM my_table WHERE name = ?", (n,))
    row = cursor.fetchone()

    if row:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Age: {row[2]}")
    else:
        print("No record found for Alice.")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


#sample from korea 
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

test.printing();
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print("Fuck Omar")
    printRowInTable("Alice")
    insertRowInTable("eljooker", 19)
    printRowInTable("eljooker")
