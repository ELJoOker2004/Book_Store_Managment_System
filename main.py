
import db_functions as db
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




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db.add_user("ahmed","1234","elbehiry")
    db.login()
    #db.add_user("ahmed","1234")
    print("Fuck Omar")
    db.printRowInTable("ahmed")
    #insertRowInTable("eljooker", 19)
    db.printRowInTable("eljooker")
    db.deleteRowInTable("2")
