from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

DB_name = "college.db"

def get_connection():
    conn = sqlite3.connect(DB_name)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    conn.execute(""" 
            CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT,
            city TEXT,
            marks INTEGER
            )
""")
    conn.commit()
    conn.close()

create_table()
students = [ ("Aman", "Bsc", "Jaipur", 78), ("priya", "bcs", "pali",88), ("rahul", "bsc", "jodhpur", 45), ("sneha", "bsc", "pali", 92), ("karan", "bca", "jaipur", 30) ]
def feed_data():
    conn = get_connection()
    conn.executemany("INSERT INTO students VALUES(?,?,?,?)",students)
    conn.commit()
    conn.close()
feed_data()
app = FastAPI()

class datavalidation(BaseModel):
    name: str 
    course: str
    city :str
    marks:int



@app.post("/studnets")
def Create_student(student:datavalidation):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO students(name , course, city, marks) VALUES(?,?,?,?)",
        (student.name,student.course,student.city, student.marks))
    # user will give the details[{"name": "Vikram", "course": "BCA", "city": "Udaipur", "marks": 67}]
    # which will be passed in the variable student and then eventually into the database 
    # vikram will get id = 6
    conn.commit()
    current_id = cursor.lastrowid
    conn.close()

# ans of B1
@app.get("/students")
def get_students():
    conn = get_connection()
    tupleee = conn.execute("SELECT name , marks FROM students WHERE marks > ? ORDER BY marks DESC", (80,)).fetchall()
    conn.close()
    return [dict(row) for row in tupleee]

# ansB3: CRUD stands for CREATE ,READ, UPDATE, DELETE,
# CREATE : CREATE TABLE IF NOT EXISTS {TABEL_NAME}
# READ: SELECT * FROM {TABLE_NAME}
# UPDATE : INSERT INTO {TBALE_NAME} WHERE {SOMETHING} IF WHERE CLAUSE NOT GIVEN EVERTHING WILL BE UPDATED 
# DELETE : DELETE FROM {TABLE_NAME} WHERE {SOMETHING}IF WHERE CLAUSE NOT GIVEN EVERTHING WILL BE DELETED
# HTTP METHODS : POST , GET , PUT , DELETE

# ANSB4

@app.get("/hello/{name}")
def hello_name(name:str):
    return {"message : name ":name} 

# ansB5

# first error = instead of concatinating use ? place holder 
# correct line  = "select * from students where id = ?", (student_id,)