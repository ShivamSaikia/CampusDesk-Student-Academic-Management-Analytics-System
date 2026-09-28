import sqlite3
from pathlib import Path
from config import DB_FILE

class DatabaseManager:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.initialize()

    def connect(self):
        return sqlite3.connect(self.db_file)

    def initialize(self):
        with self.connect() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students(
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    course TEXT NOT NULL,
                    semester INTEGER NOT NULL,
                    phone TEXT
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS marks(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    internal REAL NOT NULL,
                    assignment REAL NOT NULL,
                    lab REAL NOT NULL,
                    end_sem REAL NOT NULL,
                    total REAL NOT NULL,
                    grade TEXT NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES students(student_id)
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS attendance(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    total_classes INTEGER NOT NULL,
                    attended INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    FOREIGN KEY(student_id) REFERENCES students(student_id)
                )
            """)

    def add_student(self, data):
        with self.connect() as con:
            con.execute("""
                INSERT INTO students(student_id,name,email,course,semester,phone)
                VALUES(?,?,?,?,?,?)
            """, data)

    def update_student(self, data):
        with self.connect() as con:
            con.execute("""
                UPDATE students SET name=?, email=?, course=?, semester=?, phone=?
                WHERE student_id=?
            """, data[1:] + data[:1])

    def delete_student(self, student_id):
        with self.connect() as con:
            con.execute("DELETE FROM students WHERE student_id=?", (student_id,))
            con.execute("DELETE FROM marks WHERE student_id=?", (student_id,))
            con.execute("DELETE FROM attendance WHERE student_id=?", (student_id,))

    def get_students(self, search=""):
        with self.connect() as con:
            if search:
                return con.execute("""
                    SELECT * FROM students
                    WHERE student_id LIKE ? OR name LIKE ?
                    ORDER BY student_id
                """, (f"%{search}%", f"%{search}%")).fetchall()
            return con.execute("SELECT * FROM students ORDER BY student_id").fetchall()

    def add_marks(self, data):
        with self.connect() as con:
            con.execute("""
                INSERT INTO marks(student_id,subject,internal,assignment,lab,end_sem,total,grade)
                VALUES(?,?,?,?,?,?,?,?)
            """, data)

    def get_marks(self, student_id=None):
        with self.connect() as con:
            if student_id:
                return con.execute("""
                    SELECT student_id,subject,internal,assignment,lab,end_sem,total,grade
                    FROM marks WHERE student_id=? ORDER BY id DESC
                """, (student_id,)).fetchall()
            return con.execute("""
                SELECT student_id,subject,internal,assignment,lab,end_sem,total,grade
                FROM marks ORDER BY id DESC
            """).fetchall()

    def add_attendance(self, data):
        with self.connect() as con:
            con.execute("""
                INSERT INTO attendance(student_id,subject,total_classes,attended,percentage)
                VALUES(?,?,?,?,?)
            """, data)

    def get_attendance(self, student_id=None):
        with self.connect() as con:
            if student_id:
                return con.execute("""
                    SELECT student_id,subject,total_classes,attended,percentage
                    FROM attendance WHERE student_id=? ORDER BY id DESC
                """, (student_id,)).fetchall()
            return con.execute("""
                SELECT student_id,subject,total_classes,attended,percentage
                FROM attendance ORDER BY id DESC
            """).fetchall()

    def counts(self):
        with self.connect() as con:
            students = con.execute("SELECT COUNT(*) FROM students").fetchone()[0]
            passed = con.execute("SELECT COUNT(*) FROM marks WHERE total >= 40").fetchone()[0]
            avg_marks = con.execute("SELECT AVG(total) FROM marks").fetchone()[0] or 0
            avg_att = con.execute("SELECT AVG(percentage) FROM attendance").fetchone()[0] or 0
            return students, passed, avg_marks, avg_att
