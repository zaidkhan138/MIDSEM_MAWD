import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DB_name = "library.db"
def get_connection():
    conn = sqlite3.connect(DB_name)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    conn.execute(""" 
            CREATE TABLE IF NOT EXISTS books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            price REAL )
""")
    conn.commit()
    conn.close()


create_table()

def feed_data():
    books = [("python basics", "rao", 250),("sql guide","mehta", 180), ("web dev", "khan", 400)]
    conn = get_connection()
    conn.executemany("INSERT INTO books VALUES(?,?,?)",books)
    conn.commit()
    conn.close()
    

feed_data()

@app.put("/books/{id}")
def update_price(id:int):
    conn = get_connection()
    cursor = conn.execute("INSERT INTO books WHERE id = ?",(id,))
    # pata nahi iske age bhool gaya
    conn.commit()
    conn.close()
@app.delete("/delete")
def delete_books():
    conn = get_connection()
    conn.execute("DELETE FROM books WHERE price < 200")
    conn.execute("SELECT * FROM books")
    conn.commit()
    conn.close()


